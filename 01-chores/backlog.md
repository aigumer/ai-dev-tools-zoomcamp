# Django Household Chores Tool - Backlog

## Sprint 1: Foundation & Auth
- [ ] Set up Django project structure (done)
- [x] Configure PostgreSQL database
- [x] Create custom User model (email as username)
- [ ] Implement JWT authentication (djangorestframework-simplejwt)
- [ ] Build auth endpoints: register, login, logout, refresh token
- [ ] Add password reset flow

## Sprint 2: Core Models & Chore Management
- [ ] Create `Chore` model (title, description, frequency, assignee, created_at)
- [ ] Create `ChoreSchedule` model (chore, due_date, completed, completed_at, streak)
- [ ] Create `Frequency` choices: DAILY, WEEKLY, MONTHLY, CUSTOM
- [ ] Build Chore CRUD API endpoints
- [ ] Add chore assignment logic (only 2 users per household)

## Sprint 3: Scheduling & Calendar
- [ ] Generate recurring chore instances from frequency
- [ ] Create calendar view endpoint (month/week/day)
- [ ] Implement "due today" query
- [ ] Add overdue chore detection
- [ ] Build schedule regeneration on frequency change

## Sprint 4: Completion & Tracking
- [ ] Mark chore complete/incomplete endpoint
- [ ] Build completion history view
- [ ] Calculate and display streaks per user
- [ ] Add chore statistics (completion rate, total done)
- [ ] Create household dashboard summary

## Sprint 5: Frontend Integration (Django Templates or API for React)
- [ ] Set up Django REST Framework
- [ ] Create serializers for all models
- [ ] Add CORS configuration
- [ ] Build API documentation (drf-spectacular)
- [ ] Option A: Django templates + HTMX for simple UI
- [ ] Option B: API-only for separate React frontend

## Sprint 6: Polish & Deploy
- [ ] Add tests (unit + integration)
- [ ] Configure production settings (DEBUG=False, allowed hosts, static files)
- [ ] Set up gunicorn + nginx
- [ ] Configure SSL (Let's Encrypt)
- [ ] Add monitoring/logging
- [ ] Write deployment docs

---

## Technical Notes for Django Implementation

| Original Stack | Django Equivalent |
|---|---|
| FastAPI | Django REST Framework |
| JWT tokens | djangorestframework-simplejwt |
| PostgreSQL | PostgreSQL (same) |
| React | Django Templates + HTMX **or** DRF API for React |
| Custom auth | Custom User model + DRF auth |

## Model Sketch

```python
# myapp/models.py
class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Household(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, limit_choices_to={'is_active': True})

class Chore(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('custom', 'Custom'),
    ]
    household = models.ForeignKey(Household, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    custom_days = models.JSONField(null=True, blank=True)  # for custom frequency
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ChoreInstance(models.Model):
    chore = models.ForeignKey(Chore, on_delete=models.CASCADE)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    streak = models.IntegerField(default=0)
```