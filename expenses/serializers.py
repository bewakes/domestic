from django.contrib.auth.models import User
from rest_framework import serializers

from expenses.models import AppUser, Category, Item, Expense, Organization, Feedback


class UserSerializer(serializers.ModelSerializer):
    default_organization = serializers.SerializerMethodField(source='get_default_organization')
    organizations = serializers.SerializerMethodField(source='get_organizations')

    def get_organizations(self, user):
        return OrganizationSerializer(user.organizations, many=True).data

    def get_default_organization(self, user):
        orgs = user.organizations.filter(owner=user)
        if orgs:
            return OrganizationSerializer(orgs[0]).data
        return None

    class Meta:
        model = AppUser
        fields = ('id', 'username', 'email', 'address', 'organizations', 'default_organization')

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('id', 'user', 'content')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'organization', 'name', 'uses')

    def get_validation_exclusions(self):
        exclusions = super().get_validation_exclusions()
        return exclusions + ['description']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'organization', 'name', 'uses')
    def get_validation_exclusions(self):
        exclusions = super().get_validation_exclusions()
        return exclusions + ['description']


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name')

class ExpenseSerializer(serializers.ModelSerializer):
    # item = serializers.SerializerMethodField(source='get_item')
    # def get_item(self, expense):
    #     return ItemSerializer(expense.item).data
    date = serializers.DateTimeField(format="%Y-%m-%d")
    categoryname = serializers.SerializerMethodField(required=False, source='get_categoryname')
    items = serializers.CharField(allow_blank=True, required=False)
    modifier = serializers.SerializerMethodField(required=False, source='get_modifier')

    def get_modifier(self, expense):
        if not expense.modified_by:
            return ""
        return expense.modified_by.username

    def get_categoryname(self, expense):
        return expense.category.name

    def get_validation_exclusions(self):
        exclusions = super().get_validation_exclusions()
        return exclusions + ['description']

    class Meta:
        model = Expense
        fields = ('id', 'category', 'date', 'cost', 'categoryname', 'description', 'items', 'created_by','modified_by','modifier')

