#!/usr/bin/env python3

# Script goes here!
from models import Base, Company, Dev, Freebie
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///freebies.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Create some Companies
google = Company(name="Google", founding_year=1998)
microsoft = Company(name="Microsoft", founding_year=1975)

# Create some Devs
alice = Dev(name="Alice")
bob = Dev(name="Bob")

# Create some Freebies
freebie1 = Freebie(item_name="Laptop", value=1000, company=google, dev=alice)
freebie2 = Freebie(item_name="Headphones", value=200, company=microsoft, dev=bob)
freebie3 = Freebie(item_name="Smartwatch", value=300, company=google, dev=alice)

session.add_all([google, microsoft, alice, bob, freebie1, freebie2, freebie3])
session.commit()
