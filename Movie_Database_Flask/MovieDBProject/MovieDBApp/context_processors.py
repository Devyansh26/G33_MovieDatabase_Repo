from .models import UserProfile

def user_profile_context(request):
    """
    Context processor that adds profile information to the template context
    for authenticated users.
    """
    context = {}
    
    if request.user.is_authenticated:
        # Get or create user profile
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        # Add profile picture to context if it exists
        if profile.profile_picture:
            context['profile_picture'] = profile.profile_picture
    
    return context 