### Product
data:
- name
- flag (new, feature, sale)
- price
- image
- quantity
- reviews:
  - name
  - image
  - review
  - rate
  - date
- review count
- brand:
  - image
  - name
  - item count
- sku
- images
- subtitle
- tags
- description
- related


function:
- list
- detail
- brand list
- brand detail
- search
- filter
- add to cart
- add to wish list

---

### Users
data:
- username
- email
- image
- first name
- last name
- contact numbers:
  - type (primary - secondary)
  - number
- address:
  - type (home - office - business - academy - other)
  - address

functions:
- authentication (login - logout ...)
- dashboard
- profile
- edit profile

---

### Orders
data:
- user: FK
- order status (recieved, processed, shipped, delivered)
- code (like serial number)
- order time
- delivery time
- delivery address: FK
- coupon: FK
- total
- total_with_coupon

### Order Detail
data:
- order: FK
- product: FK
- quantity
- price
- total

### Address
data:
- user: FK
- type (home, office, work, other)
- address


### Coupon
data:
- code
- start date
- end date
- quantity
- discount