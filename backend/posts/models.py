from django.db import models


class Post(models.Model):
    body = models.CharField(max_length=350, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='postpic')
    is_private = models.BooleanField(default=False, blank=True, null=True)
    is_edited = models.BooleanField(default=False, blank=True, null=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name='parentpost', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def is_parent(self):
        return True if self.parent is None else False


class Comment(models.Model):
    body = models.CharField(max_length=300)
    post = models.ForeignKey(
        to=Post, related_name="parent_post", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_edited = models.BooleanField(default=False, blank=True, null=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, related_name='parent_child')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.body[:50]}{"..." if len(self.body) > 50 else ""}'

    @property
    def is_parent(self):
        return True if self.parent is None else False

    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-created_at').all()
