# SQLAlchemy Best Practices Implementation

## ✅ All SQLAlchemy Issues Fixed

### **1. Context Manager for Sessions** ✅
**Before:**
```python
session = DatabaseService.get_session()
try:
    # operations
    session.commit()
except:
    session.rollback()
finally:
    session.close()
```

**After:**
```python
with get_db_session() as session:
    # operations
    # Auto-commits on success, auto-rollbacks on error, auto-closes
```

**Benefits:**
- Automatic commit/rollback/close
- No memory leaks
- Cleaner code
- Exception-safe

---

### **2. Scoped Sessions for Thread Safety** ✅
**Before:**
```python
SessionLocal = sessionmaker(bind=engine)
```

**After:**
```python
SessionLocal = scoped_session(sessionmaker(bind=engine))
```

**Benefits:**
- Thread-safe for web applications
- Each thread gets its own session
- Prevents race conditions

---

### **3. Proper DateTime Defaults** ✅
**Before:**
```python
submitted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
# ❌ Evaluated at import time, not insert time
```

**After:**
```python
submitted_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
# ✅ Evaluated by database at insert time
```

**Benefits:**
- Correct timestamp on every insert
- Database-level default
- Works across all database engines

---

### **4. SQLite Connection Pool Fix** ✅
**Before:**
```python
engine = create_engine(
    DATABASE_URL,
    pool_size=10,      # ❌ Doesn't work with SQLite
    max_overflow=20    # ❌ Doesn't work with SQLite
)
```

**After:**
```python
if DATABASE_URL.startswith('sqlite'):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=20
    )
```

**Benefits:**
- Works correctly with SQLite
- Proper pooling for PostgreSQL/MySQL
- No connection errors

---

### **5. Model Relationships** ✅
**Before:**
```python
class Product_Urls(Base):
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))
    # ❌ No relationship defined
```

**After:**
```python
class Product_Urls(Base):
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))
    client: Mapped["Clients"] = relationship("Clients", back_populates="product_urls")

class Clients(Base):
    product_urls: Mapped[List["Product_Urls"]] = relationship("Product_Urls", back_populates="client")
```

**Benefits:**
- Can access `product_url.client.name` directly
- Bidirectional navigation
- Type-safe relationships

---

### **6. Eager Loading to Prevent N+1 Queries** ✅
**Before:**
```python
urls = session.query(Product_Urls).all()
for url in urls:
    print(url.client.name)  # ❌ Separate query for EACH url (N+1 problem)
```

**After:**
```python
urls = session.query(Product_Urls).options(
    joinedload(Product_Urls.client)
).all()
for url in urls:
    print(url.client.name)  # ✅ Single query with JOIN
```

**Benefits:**
- 1 query instead of N+1 queries
- Massive performance improvement
- Reduced database load

---

### **7. Module-Level Imports** ✅
**Before:**
```python
def get_all_jobs():
    from app.models.job import Job_Data  # ❌ Import inside function
    jobs = session.query(Job_Data).all()
```

**After:**
```python
# At top of file
from app.models.job import Job_Data
from app.models.clients import Clients
from app.models.product_urls import Product_Urls

def get_all_jobs():
    jobs = session.query(Job_Data).all()  # ✅ Use imported model
```

**Benefits:**
- Faster execution
- Better code organization
- Easier to maintain

---

### **8. Proper Transaction Management** ✅
**Before:**
```python
session.add(job)
session.commit()  # ❌ Commits immediately
session.add(client)
session.commit()  # ❌ Two separate transactions
```

**After:**
```python
with get_db_session() as session:
    session.add(job)
    session.add(client)
    # ✅ Both committed together in one transaction
```

**Benefits:**
- Atomic operations
- All-or-nothing guarantee
- Better data consistency

---

### **9. Foreign Key Validation** ✅
**Before:**
```python
product_url = Product_Urls(
    url=data['url'],
    client_id=data['client_id']  # ❌ No validation
)
session.add(product_url)
```

**After:**
```python
client = session.query(Clients).filter(
    Clients.id == data['client_id'],
    Clients.active == True
).first()

if not client:
    raise ValueError(f"Active client with id {data['client_id']} not found")

product_url = Product_Urls(url=data['url'], client_id=data['client_id'])
session.add(product_url)
```

**Benefits:**
- Prevents orphaned records
- Better error messages
- Data integrity

---

### **10. Bulk Operations Optimization** ✅
**Before:**
```python
for url_data in urls:
    product_url = Product_Urls(**url_data)
    session.add(product_url)
    session.commit()  # ❌ Commit for EACH item
```

**After:**
```python
product_urls = [Product_Urls(**data) for data in urls]
session.add_all(product_urls)  # ✅ Single commit for all
```

**Benefits:**
- Much faster for bulk inserts
- Single transaction
- Reduced database round-trips

---

## 🎯 Performance Improvements

### Query Optimization Examples:

#### **1. Eager Loading with Relationships**
```python
# Get product URLs with client names (1 query instead of N+1)
urls = session.query(Product_Urls).options(
    joinedload(Product_Urls.client)
).filter(Product_Urls.status == True).all()

for url in urls:
    print(f"{url.url} - {url.client.name}")  # No additional queries!
```

#### **2. Selective Column Loading**
```python
from sqlalchemy.orm import load_only

# Only load specific columns
jobs = session.query(Job_Data).options(
    load_only(Job_Data.id, Job_Data.status)
).all()
```

#### **3. Bulk Validation**
```python
# Validate all client_ids in one query
client_ids = {data['client_id'] for data in urls}
existing_clients = session.query(Clients.id).filter(
    Clients.id.in_(client_ids),
    Clients.active == True
).all()
```

---

## 📊 Before vs After Comparison

| Aspect | Before | After | Improvement |
|--------|--------|-------|-------------|
| Session Management | Manual try/finally | Context manager | ✅ Safer |
| Thread Safety | Not thread-safe | Scoped sessions | ✅ Thread-safe |
| DateTime Defaults | Import-time | Database-time | ✅ Correct |
| SQLite Pooling | Broken | Fixed | ✅ Works |
| Relationships | None | Bidirectional | ✅ Navigable |
| N+1 Queries | Yes | No (eager loading) | ✅ Fast |
| Imports | Inside functions | Module-level | ✅ Faster |
| Transactions | Multiple | Single | ✅ Atomic |
| FK Validation | None | Validated | ✅ Safe |
| Bulk Inserts | Slow | Optimized | ✅ Fast |

---

## 🚀 Usage Examples

### **Creating Records with Relationships**
```python
# Create client and product URLs in one transaction
with get_db_session() as session:
    client = Clients(name="NewClient", created_by="admin")
    session.add(client)
    session.flush()  # Get client.id without committing
    
    url1 = Product_Urls(url="https://example.com/1", client_id=client.id)
    url2 = Product_Urls(url="https://example.com/2", client_id=client.id)
    session.add_all([url1, url2])
    # Auto-commits all together
```

### **Querying with Relationships**
```python
# Get client with all their product URLs
with get_db_session() as session:
    client = session.query(Clients).options(
        joinedload(Clients.product_urls)
    ).filter(Clients.id == 2).first()
    
    print(f"Client: {client.name}")
    for url in client.product_urls:
        print(f"  - {url.url}")
```

### **Bulk Insert with Validation**
```python
urls_data = [
    {"url": "https://test1.com", "client_id": 2},
    {"url": "https://test2.com", "client_id": 2},
    {"url": "https://test3.com", "client_id": 3}
]

result = DatabaseService.create_product_urls_bulk(urls_data)
print(f"Created {result['created']} URLs")
```

---

## 🔍 Testing the Improvements

### **Test Eager Loading**
```python
# Enable SQL logging to see queries
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# This should show only 1 query with JOIN
urls = DatabaseService.get_all_product_urls(page=1, page_size=10)
```

### **Test Context Manager**
```python
# This should auto-rollback on error
try:
    with get_db_session() as session:
        client = Clients(name="Test")
        session.add(client)
        raise Exception("Simulated error")
except:
    pass

# Client should NOT be in database (rolled back)
```

---

## 📝 Migration Notes

### **No Breaking Changes**
- All API endpoints work exactly the same
- Response formats unchanged
- Only internal implementation improved

### **Database Schema**
- No schema changes required
- Existing data works as-is
- Relationships are ORM-level only

### **Performance**
- Queries are now faster (eager loading)
- Bulk operations are optimized
- Memory usage is better (context managers)

---

## 🎓 Key Takeaways

1. **Always use context managers** for database sessions
2. **Use scoped_session** for web applications
3. **Define relationships** between models
4. **Use eager loading** to prevent N+1 queries
5. **Import models at module level**, not inside functions
6. **Use server_default** for DateTime fields
7. **Validate foreign keys** before inserting
8. **Use bulk operations** for multiple inserts
9. **Handle SQLite differently** from other databases
10. **Let context managers handle** commit/rollback/close

---

## 🔗 Additional Resources

- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/orm/tutorial.html)
- [Relationship Loading Techniques](https://docs.sqlalchemy.org/en/20/orm/loading_relationships.html)
- [Session Basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
