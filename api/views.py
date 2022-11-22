from books.models import BookReview
from api.serializers import BookReviewSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

class BookReviewDetailAPIView(APIView):
    def get(self, request, id):
        book_review = BookReview.objects.get(id=id)

        serializer = BookReviewSerializer(book_review)

#        json_response = {
#            'id': book_review.id,
#            'stars_given': book_review.stars_given,
#            'comment': book_review.comment,
#            'book': {
#                'id':book_review.book.id,
#                'title': book_review.book.title,
#                'description': book_review.book.description,
#                'isbn': book_review.book.isbn
#            },
#            'user': {
#                'id': book_review.user.id,
#                'first_name': book_review.user.first_name,
#                'last_name': book_review.user.last_name,
#                'username': book_review.user.username
#            }
#        }

        return Response(data=serializer.data)

class BookListAPIView(APIView):
    def get(self, request):
        book_reviews = BookReview.objects.all()
        serializer = BookReviewSerializer(book_reviews, many=True)
        return Response(data=serializer.data)

