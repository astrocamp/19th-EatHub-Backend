import random
from concurrent.futures import ThreadPoolExecutor, as_completed

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Favorite, User
from users.utils import optional_token_cbv, token_required_cbv
from utilities.cloudinary_upload import upload_to_cloudinary
from utilities.openai_api import find_dish, openai_api
from utilities.place_api import get_google_photo, get_place_details, text_search

from .models import Restaurant
from .serializers import FullRestaurantSerializer, RestaurantDetailSerializer, ReviewSerializer


class RecommendRestaurants(APIView):
    def post(self, request):
        data = request.data
        flavors = data['flavors']
        mains = data['mains']
        staples = data['staples']
        latitude = data['user_location']['latitude']
        longitude = data['user_location']['longitude']
        location = f'{latitude},{longitude}'
        keywords = openai_api(find_dish(flavors, mains, staples)).split(',')
        random.shuffle(keywords)
        selected_restaurants = None

        for keyword in keywords:
            recommend_dish = keyword
            restaurants = text_search(keyword, location, 800, count=12)

            if len(restaurants) >= 12:
                selected_restaurants = restaurants
                break

        place_ids = [place['place_id'] for place in selected_restaurants]
        existing_restaurants = Restaurant.objects.filter(place_id__in=place_ids).only(
            'place_id', 'image_url'
        )
        image_map = {
            restaurant.place_id: restaurant.image_url
            for restaurant in existing_restaurants
            if restaurant.image_url
        }
        missing_image_ids = set(place_ids) - set(image_map.keys())
        places_need_image = [
            place for place in selected_restaurants if place['place_id'] in missing_image_ids
        ]

        def fetch_and_upload_image(place):
            place_id = place['place_id']
            photo_ref = place.get('google_photo_reference')
            if not photo_ref:
                return (place_id, None)

            photo_bytes = get_google_photo(photo_ref)
            if not photo_bytes:
                return (place_id, None)

            try:
                image_url = upload_to_cloudinary(photo_bytes, filename=place_id)
                return (place_id, image_url)
            except Exception:
                return (place_id, None)

        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = [
                executor.submit(fetch_and_upload_image, place) for place in places_need_image
            ]
            for future in as_completed(futures):
                place_id, url = future.result()
                if url:
                    image_map[place_id] = url

        restaurant_instances = []

        for place in selected_restaurants:
            place['image_url'] = image_map.get(place['place_id'])
            restaurant, _ = Restaurant.objects.update_or_create(
                place_id=place['place_id'], defaults=place
            )
            restaurant_instances.append(restaurant)

        serializer = FullRestaurantSerializer(restaurant_instances, many=True)
        data = serializer.data

        return Response(
            {'result': {'dish': recommend_dish, 'restaurants': serializer.data}},
            status=status.HTTP_200_OK,
        )


class CreateReview(APIView):
    @token_required_cbv
    def post(self, request, restaurant_uuid):
        restaurant = get_object_or_404(Restaurant, uuid=restaurant_uuid)
        user = User.objects.get(uuid=request.user_uuid)

        serializer = ReviewSerializer(
            data=request.data, context={'user': user, 'restaurant': restaurant, 'request': request}
        )
        if serializer.is_valid():
            review = serializer.save()
            return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)


class RestaurantDetailView(APIView):
    @optional_token_cbv
    def get(self, request, uuid):
        restaurant = get_object_or_404(Restaurant, uuid=uuid)

        if not restaurant.phone or not restaurant.open_hours:
            details = get_place_details(restaurant.place_id)
            if 'error' not in details:
                restaurant.phone = details.get('phone') or restaurant.phone
                restaurant.open_hours = details.get('opening_hours')
                restaurant.save()

        serializer = RestaurantDetailSerializer(restaurant, context={'request': request})
        return Response({'result': serializer.data})


class FavoriteRestaurantView(APIView):
    @token_required_cbv
    def post(self, request, uuid):
        user = get_object_or_404(User, uuid=request.user_uuid)
        restaurant = get_object_or_404(Restaurant, uuid=uuid)

        if Favorite.objects.filter(user=user, restaurant=restaurant).exists():
            return Response({'success': False}, status=status.HTTP_200_OK)

        Favorite.objects.create(user=user, restaurant=restaurant)

        return Response({'success': True}, status=status.HTTP_201_CREATED)

    @token_required_cbv
    def delete(self, request, uuid):
        user = get_object_or_404(User, uuid=request.user_uuid)
        restaurant = get_object_or_404(Restaurant, uuid=uuid)
        favorite = Favorite.objects.filter(user=user, restaurant=restaurant).first()

        if favorite:
            favorite.delete()
            return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)
        return Response({'success': False}, status=status.HTTP_200_OK)


class RecentViewedRestaurantsView(APIView):
    def get(self, request):
        uuid_list = request.query_params.getlist('uuids')

        if not uuid_list:
            return Response({'result': []}, status=status.HTTP_200_OK)

        restaurants = Restaurant.objects.filter(uuid__in=uuid_list)
        restaurant_map = {str(r.uuid): r for r in restaurants}

        sorted_restaurants = [restaurant_map[uuid] for uuid in uuid_list if uuid in restaurant_map]

        serializer = FullRestaurantSerializer(sorted_restaurants, many=True)
        return Response({'result': serializer.data}, status=status.HTTP_200_OK)
