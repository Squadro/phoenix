from django.db import models


class LastSuccessfulPage(models.Model):
    page_number = models.IntegerField()

    class Meta:
        # Additional options for the model
        db_table = "last_successful_page"  # Set the database table name

    def __str__(self):
        # String representation of the model instance
        return f"Last Successful Page: {self.page_number}"
