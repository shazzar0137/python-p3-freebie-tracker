#!/usr/bin/env python3

#!/usr/bin/env python3
from models import Company, Dev, Freebie
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Retrieve objects
    dev = session.query(Dev).filter_by(name="Alice").first()
    company = session.query(Company).filter_by(name="Google").first()

    # Test received_one()
    print(dev.received_one("Laptop"))  # output: True
    print(dev.received_one("Tablet"))  # output: False

    # Test give_away()
    freebie = session.query(Freebie).filter_by(item_name="Laptop").first()
    dev.give_away(session.query(Dev).filter_by(name="Bob").first(), freebie)
    session.commit()

    # Test print_details()
    print(freebie.print_details())  # Should show Bob owns a Laptop from Google

    # Test oldest_company()
    print(Company.oldest_company(session)) #output: microsoft
    import ipdb; ipdb.set_trace()
