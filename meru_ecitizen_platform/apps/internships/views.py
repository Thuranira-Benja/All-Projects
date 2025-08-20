from rest_framework import generics
from .models import InternshipPost, StudentProfile
from .serializers import InternshipPostSerializer # You will need to create this
from .services import calculate_match_score

class InternshipMatchView(generics.ListAPIView):
    serializer_class = InternshipPostSerializer

    def get_queryset(self):
        user = self.request.user
        try:
            student_profile = StudentProfile.objects.get(user=user)
        except StudentProfile.DoesNotExist:
            return InternshipPost.objects.none() # Return no matches if no profile

        active_posts = InternshipPost.objects.filter(is_active=True)
        
        # Calculate scores and sort
        scored_posts = []
        for post in active_posts:
            score = calculate_match_score(student_profile, post)
            if score > 0.2: # Only show posts with a reasonable match score
                post.match_score = score # Annotate the object
                scored_posts.append(post)
        
        # Sort by the highest match score
        return sorted(scored_posts, key=lambda p: p.match_score, reverse=True)