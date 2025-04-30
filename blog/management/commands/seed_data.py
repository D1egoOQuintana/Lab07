from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from blog.models import Category, Tag, Post, Comment
import random
from datetime import timedelta


class Command(BaseCommand):
    """Command to seed the database with sample data"""
    help = 'Seeds the database with sample data for development and testing'
    
    def handle(self, *args, **options):
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            self.stdout.write('Creating superuser... 👤')
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
        
        # Create regular user if it doesn't exist
        if not User.objects.filter(username='user').exists():
            self.stdout.write('Creating regular user... 👤')
            User.objects.create_user(
                username='user',
                email='user@example.com',
                password='user123'
            )

        # Create categories
        self.stdout.write('Creating categories... 📂')
        categories = [
            ('Programming', 'Posts about programming languages and software development.'),
            ('Web Development', 'Content about web technologies and frameworks.'),
            ('Data Science', 'Articles related to data analysis and machine learning.'),
            ('DevOps', 'Topics covering deployment and operations.'),
            ('Career', 'Career advice and professional development tips.'),
        ]

        for name, description in categories:
            Category.objects.get_or_create(
                name=name,
                defaults={
                    'slug': slugify(name),
                    'description': description
                }
            )

        # Create tags
        self.stdout.write('Creating tags... 🏷️')
        tags = [
            'Python', 'Django', 'JavaScript', 'React', 'Docker',
            'Git', 'Database', 'API', 'Testing', 'Security',
            'Frontend', 'Backend', 'Cloud', 'AI', 'Machine Learning'
        ]

        created_tags = []
        for tag_name in tags:
            tag, _ = Tag.objects.get_or_create(
                name=tag_name,
                defaults={'slug': slugify(tag_name)}
            )
            created_tags.append(tag)

        # Get users
        admin_user = User.objects.get(username='admin')
        regular_user = User.objects.get(username='user')

        # Create sample posts with more detailed content
        self.stdout.write('Creating posts... 📝')
        posts_data = [
            {
                'title': 'Mastering Django ORM Relationships',
                'content': '''
                Django's ORM is one of its most powerful features. Let's explore how to master relationships in Django.

                ## Key Types of Relationships

                1. One-to-Many (ForeignKey)
                2. Many-to-Many
                3. One-to-One

                ## Best Practices

                - Always define related_name
                - Use appropriate on_delete behavior
                - Consider database indexes
                - Use select_related and prefetch_related
                ''',
                'author': admin_user,
                'category': 'Programming',
                'tags': ['Python', 'Django', 'Database'],
                'status': 'published'
            },
            {
                'title': 'Modern Frontend Development with React',
                'content': '''
                React has revolutionized how we build user interfaces. Here's what you need to know.

                ## Key Concepts

                1. Components
                2. State Management
                3. Hooks
                4. Virtual DOM

                ## Best Practices

                - Keep components small
                - Use functional components
                - Implement proper state management
                - Optimize performance
                ''',
                'author': regular_user,
                'category': 'Web Development',
                'tags': ['JavaScript', 'React', 'Frontend'],
                'status': 'published'
            },
            {
                'title': 'DevOps Best Practices with Docker',
                'content': '''
                Docker has changed how we deploy applications. Let's explore best practices.

                ## Key Concepts

                1. Containers
                2. Images
                3. Docker Compose
                4. Orchestration

                ## Best Practices

                - Use multi-stage builds
                - Optimize image size
                - Implement proper logging
                - Secure your containers
                ''',
                'author': admin_user,
                'category': 'DevOps',
                'tags': ['Docker', 'DevOps', 'Cloud'],
                'status': 'published'
            }
        ]

        for data in posts_data:
            category = Category.objects.get(name=data['category'])
            published_at = timezone.now() - timedelta(days=random.randint(1, 30)) if data['status'] == 'published' else None
            
            post, created = Post.objects.get_or_create(
                title=data['title'],
                defaults={
                    'slug': slugify(data['title']),
                    'content': data['content'],
                    'author': data['author'],
                    'category': category,
                    'status': data['status'],
                    'published_at': published_at
                }
            )

            if created:
                # Add tags
                for tag_name in data['tags']:
                    tag = Tag.objects.get(name=tag_name)
                    post.tags.add(tag)
                self.stdout.write(f"  Created post: {post.title} ✅")

        # Create comments with meaningful content
        self.stdout.write('Creating comments... 💬')
        comments_data = [
            {
                'content': "Great article! This really helped me understand the concept better.",
                'author': regular_user
            },
            {
                'content': "Could you elaborate more on the best practices section?",
                'author': admin_user
            },
            {
                'content': "I've implemented this in my project and it works perfectly!",
                'author': regular_user
            },
            {
                'content': "Very well explained. The examples are particularly helpful.",
                'author': admin_user
            },
            {
                'content': "Looking forward to more articles like this!",
                'author': regular_user
            }
        ]

        for post in Post.objects.filter(status='published'):
            # Create 2-4 random comments per post
            num_comments = random.randint(2, 4)
            for _ in range(num_comments):
                comment_data = random.choice(comments_data)
                Comment.objects.create(
                    post=post,
                    author=comment_data['author'],
                    content=comment_data['content'],
                    is_approved=True
                )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully! 🎉'))
        self.stdout.write('\nYou can now log in with:')
        self.stdout.write('Admin user -> username: admin, password: admin123')
        self.stdout.write('Regular user -> username: user, password: user123')
