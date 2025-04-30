# Django Blog Platform with ORM Mastery

A step-by-step guide to building a blog platform with Django, focusing on mastering the ORM system through practical implementation. Learn how to create models with different relationship types, implement custom managers, perform complex queries, and leverage the power of Django's ORM for efficient data manipulation. Perfect for beginners and intermediate developers wanting to strengthen their Django data handling skills.

## Table of Contents

- [Django Blog Platform with ORM Mastery](#django-blog-platform-with-orm-mastery)
  - [Table of Contents](#table-of-contents)
  - [1. Understanding the Concept](#1-understanding-the-concept)
    - [What is Django ORM?](#what-is-django-orm)
    - [Relationship Types in Django](#relationship-types-in-django)
    - [Why a Blog Platform?](#why-a-blog-platform)
    - [Application Structure](#application-structure)
  - [2. Environment Setup](#2-environment-setup)
    - [Creating Project Structure](#creating-project-structure)
    - [Installing Dependencies](#installing-dependencies)
    - [Git Configuration](#git-configuration)
  - [3. Implementation](#3-implementation)
    - [Step 1: Project Creation](#step-1-project-creation)
    - [Step 2: Creating the Blog App](#step-2-creating-the-blog-app)
    - [Step 3: Defining Models](#step-3-defining-models)
    - [Step 4: Creating Custom Managers](#step-4-creating-custom-managers)
    - [Step 5: Implementing Admin Interface](#step-5-implementing-admin-interface)
    - [Step 6: Creating Views](#step-6-creating-views)
    - [Step 7: Adding URL Patterns](#step-7-adding-url-patterns)
    - [Step 8: Creating Basic Templates](#step-8-creating-basic-templates)

## 1. Understanding the Concept

### What is Django ORM?

Django's Object-Relational Mapping (ORM) is a powerful abstraction layer that allows you to interact with your database using Python code instead of writing raw SQL queries. Key features include:

1. **Model Definition** - Define database structure using Python classes
2. **Query API** - Simple, intuitive API for database queries
3. **Migration System** - Track and apply database schema changes
4. **Relationship Handling** - Easy management of related data
5. **Lazy Loading** - Query execution only when needed

The ORM is one of Django's most powerful features, allowing developers to focus on business logic rather than database operations.

### Relationship Types in Django

Django ORM supports various relationship types:

1. **One-to-Many (ForeignKey)**
   ```
   Post ─→ Category (One category has many posts)
   ```

2. **Many-to-Many (ManyToManyField)**
   ```
   Post ↔ Tag (Posts have multiple tags, tags belong to multiple posts)
   ```

3. **One-to-One (OneToOneField)**
   ```
   User ─── Profile (One user has exactly one profile)
   ```

### Why a Blog Platform?

A blog platform is ideal for learning Django ORM because:

1. It involves multiple related models (posts, categories, tags, comments)
2. It requires various query patterns (filtering, ordering, annotations)
3. It utilizes both simple and complex relationships
4. It's a familiar concept that's easy to visualize
5. It provides practical experience with common data operations

### Application Structure

Our blog platform will have the following structure:

```
blog_platform/                # Project root
├── src/                      # Source code directory
│   ├── config/               # Project settings
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── blog/                 # Blog application
│   │   ├── __init__.py
│   │   ├── admin.py          # Admin configuration
│   │   ├── apps.py
│   │   ├── management/       # Management commands
│   │   │   └── commands/
│   │   │       └── seed_data.py
│   │   ├── migrations/       # Database migrations
│   │   ├── models.py         # Data models
│   │   ├── urls.py           # URL patterns
│   │   └── views.py          # View functions
│   ├── templates/            # HTML templates
│   │   └── blog/
│   │       ├── base.html     # Base template
│   │       ├── post_list.html
│   │       └── post_detail.html
│   └── manage.py             # Django command-line utility
├── venv/                     # Virtual environment
└── requirements.txt          # Python dependencies
```

## 2. Environment Setup

### Creating Project Structure

Let's set up our development environment:

```bash
# Create project directory
mkdir -p blog_platform
cd blog_platform

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Create src directory
mkdir src
cd src
```

### Installing Dependencies

Install Django and required packages:

```bash
# Install Django
pip3 install django

# Create requirements file
pip3 freeze > ../requirements.txt
```

### Git Configuration

Create a `.gitignore` file in the project root:

```bash
# Navigate to project root
cd ..

# Create .gitignore file
cat > .gitignore << EOL
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media/

# Miscellaneous
.DS_Store
.env
.idea/
.vscode/
EOL
```

## 3. Implementation

### Step 1: Project Creation

Create a new Django project:

```bash
# Navigate to src directory
cd src

# Create Django project
django-admin startproject config .
```

This creates the basic Django project structure including the `config` directory and `manage.py`.

### Step 2: Creating the Blog App

Create the blog application:

```bash
# Create blog app
python3 manage.py startapp blog
```

Register the app in `config/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',  # Our blog app
]

# Add template directory configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Add this line
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

### Step 3: Defining Models

Create the models for our blog platform in `blog/models.py`:

```python
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """Category model for organizing blog posts"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:category_detail', args=[self.slug])


class Tag(models.Model):
    """Tag model for categorizing blog posts"""
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:tag_detail', args=[self.slug])


class PostManager(models.Manager):
    """Custom manager for Post model"""
    
    def published(self):
        """Return only published posts"""
        return self.filter(status='published')
    
    def by_category(self, category_slug):
        """Return posts for a specific category"""
        return self.published().filter(category__slug=category_slug)
    
    def by_tag(self, tag_slug):
        """Return posts with a specific tag"""
        return self.published().filter(tags__slug=tag_slug).distinct()
    
    def recent_posts(self, count=5):
        """Return most recent posts"""
        return self.published().order_by('-published_date')[:count]


class Post(models.Model):
    """Blog post model"""
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    
    # Relationships
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    
    # Custom manager
    objects = models.Manager()  # Default manager
    published_objects = PostManager()  # Custom manager
    
    class Meta:
        ordering = ['-published_date']
        indexes = [
            models.Index(fields=['-published_date']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])
    
    @property
    def comment_count(self):
        """Return the number of comments for this post"""
        return self.comments.filter(approved=True).count()


class Comment(models.Model):
    """Comment model for blog posts"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_date']
        indexes = [
            models.Index(fields=['created_date']),
        ]
    
    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
```

### Step 4: Creating Custom Managers

We've already defined a custom manager for the Post model in the previous step. Let's add a custom manager for the Comment model in `blog/models.py`:

```python
class CommentManager(models.Manager):
    """Custom manager for Comment model"""
    
    def approved(self):
        """Return only approved comments"""
        return self.filter(approved=True)
    
    def recent_comments(self, count=5):
        """Return most recent approved comments"""
        return self.approved().order_by('-created_date')[:count]

# Add this manager to the Comment model
class Comment(models.Model):
    # ... existing code ...
    
    # Custom manager
    objects = models.Manager()  # Default manager
    approved_objects = CommentManager()  # Custom manager
    
    # ... rest of the class ...
```

### Step 5: Implementing Admin Interface

Create an admin interface in `blog/admin.py`:

```python
from django.contrib import admin
from .models import Category, Tag, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'published_date')
    list_filter = ('status', 'category', 'published_date', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'published_date'
    filter_horizontal = ('tags',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created_date', 'approved')
    list_filter = ('approved', 'created_date')
    search_fields = ('name', 'email', 'content')
    actions = ['approve_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    approve_comments.short_description = "Approve selected comments"
```

### Step 6: Creating Views

Create views in `blog/views.py`:

```python
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Count
from .models import Post, Category, Tag


class PostListView(ListView):
    """View for listing blog posts"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        """Get only published posts"""
        return Post.published_objects.published()
    
    def get_context_data(self, **kwargs):
        """Add additional context data"""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.annotate(post_count=Count('posts')).order_by('-post_count')[:10]
        context['recent_posts'] = Post.published_objects.recent_posts()
        return context


class PostDetailView(DetailView):
    """View for displaying a single post"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        """Get only published posts"""
        return Post.published_objects.published()
    
    def get_context_data(self, **kwargs):
        """Add additional context data"""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.annotate(post_count=Count('posts')).order_by('-post_count')[:10]
        context['recent_posts'] = Post.published_objects.recent_posts()
        return context


class CategoryPostListView(ListView):
    """View for listing posts in a specific category"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        """Get published posts for a specific category"""
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.published_objects.by_category(self.category.slug)
    
    def get_context_data(self, **kwargs):
        """Add additional context data"""
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.annotate(post_count=Count('posts')).order_by('-post_count')[:10]
        context['recent_posts'] = Post.published_objects.recent_posts()
        return context


class TagPostListView(ListView):
    """View for listing posts with a specific tag"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        """Get published posts with a specific tag"""
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.published_objects.by_tag(self.tag.slug)
    
    def get_context_data(self, **kwargs):
        """Add additional context data"""
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.annotate(post_count=Count('posts')).order_by('-post_count')[:10]
        context['recent_posts'] = Post.published_objects.recent_posts()
        return context
```

### Step 7: Adding URL Patterns

Create `blog/urls.py` to define URL patterns:

```python
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Home page (post list)
    path('', views.PostListView.as_view(), name='post_list'),
    
    # Post detail page
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    
    # Category detail page
    path('category/<slug:slug>/', views.CategoryPostListView.as_view(), name='category_detail'),
    
    # Tag detail page
    path('tag/<slug:slug>/', views.TagPostListView.as_view(), name='tag_detail'),
]
```

Update `config/urls.py` to include the blog app URLs:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]
```

### Step 8: Creating Basic Templates

Create basic templates for our blog platform:

1. Create the directory structure:

```bash
mkdir -p templates/blog
```

2. Create `templates/blog/base.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Django Blog Platform{% endblock %}</title>
    <style>
        /* Simple dark theme */
        :root {
            --color-primary: #23B5E8;
            --color-secondary: #234B96;
            --color-black: #010508;
            --color-dark: #121212;
            --color-dark-lighter: #1E1E1E;
            --color-text: #E0E0E0;
            --color-text-muted: #AAAAAA;
        }
        
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: var(--color-text);
            background-color: var(--color-black);
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        /* Header */
        .header {
            background-color: var(--color-dark);
            padding: 1rem;
            margin-bottom: 1rem;
            border-bottom: 2px solid var(--color-primary);
        }
        .header__title {
            color: var(--color-primary);
            text-decoration: none;
        }
        
        /* Layout */
        .layout {
            display: flex;
            flex-wrap: wrap;
        }
        .layout__main {
            flex: 3;
            min-width: 60%;
        }
        .layout__sidebar {
            flex: 1;
            min-width: 250px;
            margin-left: 1rem;
            background-color: var(--color-dark-lighter);
            padding: 1rem;
            border-radius: 4px;
        }
        
        /* Post */
        .post {
            background-color: var(--color-dark-lighter);
            border-left: 3px solid var(--color-primary);
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 0 4px 4px 0;
        }
        .post__title {
            color: var(--color-primary);
            margin-top: 0;
        }
        .post__link {
            color: var(--color-primary);
            text-decoration: none;
        }
        .post__meta {
            color: var(--color-text-muted);
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }
        .post__content {
            margin-top: 1rem;
        }
        
        /* Sidebar */
        .sidebar__section {
            margin-bottom: 2rem;
        }
        .sidebar__title {
            color: var(--color-primary);
            border-bottom: 1px solid var(--color-secondary);
            padding-bottom: 0.5rem;
        }
        .sidebar__list {
            list-style: none;
            padding: 0;
        }
        .sidebar__item {
            margin-bottom: 0.5rem;
        }
        .sidebar__link {
            color: var(--color-text);
            text-decoration: none;
        }
        .sidebar__link:hover {
            color: var(--color-primary);
        }
        
        /* Tags */
        .tag {
            display: inline-block;
            background-color: var(--color-secondary);
            color: var(--color-text);
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            margin: 0 0.5rem 0.5rem 0;
            font-size: 0.8rem;
            text-decoration: none;
        }
        
        /* Comments */
        .comments {
            margin-top: 2rem;
        }
        .comment {
            background-color: var(--color-dark);
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 4px;
        }
        .comment__meta {
            color: var(--color-text-muted);
            font-size: 0.8rem;
            margin-bottom: 0.5rem;
        }
        
        /* Footer */
        .footer {
            background-color: var(--color-dark);
            color: var(--color-text-muted);
            padding: 1rem;
            margin-top: 2rem;
            text-align: center;
            border-top: 2px solid var(--color-secondary);
        }
        
        /* Pagination */
        .pagination {
            margin-top: 2rem;
            display: flex;
            justify-content: center;
        }
        .pagination__link {
            background-color: var(--color-dark);
            color: var(--color-text);
            padding: 0.5rem 1rem;
            margin: 0 0.25rem;
            text-decoration: none;
            border-radius: 4px;
        }
        .pagination__link--active {
            background-color: var(--color-primary);
        }
    </style>
</head>
<body>
    <header class="header">
        <h1><a href="{% url 'blog:post_list' %}" class="header__title">Django Blog Platform</a></h1>
    </header>
    
    <div class="layout">
        <main class="layout__main">
            {% block content %}
            <!-- Main content will go here -->
            {% endblock %}
        </main>
        
        <aside class="layout__sidebar">
            <section class="sidebar__section">
                <h3 class="sidebar__title">Categories</h3>
                <ul class="sidebar__list">
                    {% for category in categories %}
                        <li class="sidebar__item">
                            <a href="{% url 'blog:category_detail' category.slug %}" class="sidebar__link">{{ category.name }}</a>
                        </li>
                    {% empty %}
                        <li class="sidebar__item">No categories available</li>
                    {% endfor %}
                </ul>
            </section>
            
            <section class="sidebar__section">
                <h3 class="sidebar__title">Recent Posts</h3>
                <ul class="sidebar__list">
                    {% for post in recent_posts %}
                        <li class="sidebar__item">
                            <a href="{% url 'blog:post_detail' post.slug %}" class="sidebar__link">{{ post.title }}</a>
                        </li>
                    {% empty %}
                        <li class="sidebar__item">No recent posts</li>
                    {% endfor %}
                </ul>
            </section>
            
            <section class="sidebar__section">
                <h3 class="sidebar__title">Popular Tags</h3>
                <div>
                    {% for tag in tags %}
                        <a href="{% url 'blog:tag_detail' tag.slug %}" class="tag">{{ tag.name }}</a>
                    {% empty %}
                        <p>No tags available</p>
                    {% endfor %}
                </div>
            </section>
        </aside>
    </div>
    
    <footer class="footer">
        <p>&copy; {% now "Y" %} Django Blog Platform - A learning project</p>
    </footer>
</body>
</html>
```

3. Create `templates/blog/post_list.html`:

```html
{% extends "blog/base.html" %}

{% block title %}
    {% if category %}
        Posts in {{ category.name }} - Django Blog
    {% elif tag %}
        Posts tagged with {{ tag.name }} - Django Blog
    {% else %}
        Blog Posts - Django Blog
    {% endif %}
{% endblock %}

{% block content %}
    {% if category %}
        <h2>Posts in category: {{ category.name }}</h2>
    {% elif tag %}
        <h2>Posts tagged with: {{ tag.name }}</h2>
    {% else %}
        <h2>Latest Posts</h2>
    {% endif %}
    
    {% for post in posts %}
        <article class="post">
            <h3 class="post__title">
                <a href="{{ post.get_absolute_url }}" class="post__link">{{ post.title }}</a>
            </h3>
            
            <div class="post__meta">
                <span>Posted by {{ post.author.username }}</span>
                <span>in <a href="{% url 'blog:category_detail' post.category.slug %}">{{ post.category.name }}</a></span>
                <span>on {{ post.published_date|date:"F j, Y" }}</span>
            </div>
            
            <div class="post__content">
                {{ post.content|truncatewords:50|linebreaks }}
                <a href="{{ post.get_absolute_url }}" class="post__link">Read more</a>
            </div>
            
            {% if post.tags.all %}
                <div class="post__tags">
                    {% for tag in post.tags.all %}
                        <a href="{% url 'blog:tag_detail' tag.slug %}" class="tag">{{ tag.name }}</a>
                    {% endfor %}
                </div>
            {% endif %}
        </article>
    {% empty %}
        <p>No posts available.</p>
    {% endfor %}
    
    {% if is_paginated %}
        <div class="pagination">
            {% if page_obj.has_previous %}
                <a href="?page={{ page_obj.previous_page_number }}" class="pagination__link">&laquo; Previous</a>
            {% endif %}
            
            {% for i in paginator.page_range %}
                {% if page_obj.number == i %}
                    <a class="pagination__link pagination__link--active">{{ i }}</a>
                {% else %}
                    <a href="?page={{ i }}" class="pagination__link">{{ i }}</a>
                {% endif %}
            {% endfor %}
            
            {% if page_obj.has_next %}
                <a href="?page={{ page_obj.next_page_number }}" class="pagination__link">Next &raquo;</a>
            {% endif %}
        </div>
    {% endif %}
{% endblock %}
```

4. Create `templates/blog/post_detail.html`:

```html
{% extends "blog/base.html" %}

{% block title %}{{ post.title }} - Django Blog{% endblock %}

{% block content %}
    <article class="post">
        <h2 class="post__title">{{ post.title }}</h2>
        
        <div class="post__meta">
            <span>Posted by {{ post.author.username }}</span>
            <span>in <a href="{% url 'blog:category_detail' post.category.slug %}">{{ post.category.name }}</a></span>
            <span>on {{ post.published_date|date:"F j, Y" }}</span>
        </div>
        
        <div class="post__content">
            {{ post.content|linebreaks }}
        </div>
        
        {% if post.tags.all %}
            <div class="post__tags">
                <h4>Tags:</h4>
                {% for tag in post.tags.all %}
                    <a href="{% url 'blog:tag_detail' tag.slug %}" class="tag">{{ tag.name }}</a>
                {% endfor %}
            </div>
        {% endif %}
    </article>
    
    <section class="comments">
        <h3>Comments ({{ post.comment_count }})</h3>
        
        {% for comment in post.comments.all %}
            {% if comment.approved %}
                <div class="comment">
                    <div class="comment__meta">
                        {{ comment.name }} on {{ comment.created_date|date:"F j, Y" }}
                    </div>
                    <div class="comment__content">
                        {{ comment.content|linebreaks }}
                    </div>
                </div>
            {% endif %}
        {% empty %}
            <p>No comments yet. Be the first to comment!</p>
        {% endfor %}
    </section>
{% endblock %}
