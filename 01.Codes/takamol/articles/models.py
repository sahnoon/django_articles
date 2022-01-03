from django.db import models


class Articles(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    body = models.TextField()
    date = models.DateTimeField()
    url_to_image = models.ImageField(blank=True)

    def __str__(self):
        """to show the article title in the querey set
        """
        return self.title

    def snippet(self):
        """return a part of article body

        Returns:
            str: snippet
        """
        return self.body[:50] + '...'
