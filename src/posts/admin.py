from django.contrib import admin

from .models import Post, Comment, Tag, PostImage, Category


class PostImageInline(admin.TabularInline):
    model = PostImage


class PostAdmin(admin.ModelAdmin):
        inlines = [PostImageInline,]
        list_display = ('title', 'created', 'published', 'categories', 'live_link',)
        prepopulated_fields = {'slug': ('title',)}
        search_fields = ['title', 'created', 'category__title']
        list_filter = ['created',]

        readonly_fields = ['categories', 'live_link']

        class Meta:
            model = Post

        def categories(self, obj):
            cat = []
            for i in obj.category_set.all():
                link = "<a href='/admin/posts/category/" + str(i.id) + "/'>" + i.title + "</a>"
                cat.append(link)
            return ", ".join(cat)

        categories.allow_tags = True

        def live_link(self, obj):
            link = "<a href='/posts/" + str(obj.slug) + "/'>" + obj.title + "</a>"
            return link

        live_link.allow_tags = True

admin.site.register(Post, PostAdmin)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

    class Meta:
        model = Category

admin.site.register(Category, CategoryAdmin)


class CommentAdmin(admin.ModelAdmin):
    display_fields = ["post", "username", "created"]

    class Meta:
        model = Comment

admin.site.register(Comment, CommentAdmin)


class PostImageAdmin(admin.ModelAdmin):
    class Meta:
        model = PostImage

admin.site.register(PostImage, PostImageAdmin)


class TagAdmin(admin.ModelAdmin):
    class Meta:
        model = Tag

admin.site.register(Tag, TagAdmin)