from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

# Naming convention for migrations
convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

# Association Table
company_dev = Table(
    'company_dev',
    Base.metadata,
    Column('company_id', ForeignKey('companies.id'), primary_key=True),
    Column('dev_id', ForeignKey('devs.id'), primary_key=True),
    extend_existing=True,
)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)
    founding_year = Column(Integer(), nullable=False)

    freebies = relationship("Freebie", backref="company")
    devs = relationship("Dev", secondary=company_dev, back_populates="companies")

    def __repr__(self):
        return f'<Company {self.name}>'

    def give_freebie(self, dev, item_name, value):
        #Creates a new Freebie instance associated with this company and the given dev.
        freebie = Freebie(item_name=item_name, value=value, company=self, dev=dev)
        return freebie

    @classmethod
    def oldest_company(cls, session):
        #Returns the Company instance with the earliest founding year.
        return session.query(cls).order_by(cls.founding_year).first()

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)

    freebies = relationship("Freebie", backref="dev")
    companies = relationship("Company", secondary=company_dev, back_populates="devs")

    def __repr__(self):
        return f'<Dev {self.name}>'
    
    def received_one(self, item_name):
        #Returns True if the dev has received a Freebie with the given item_name.
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, dev, freebie):
        #Transfers a freebie to another dev if the freebie belongs to the current dev.
        if freebie in self.freebies:
            freebie.dev = dev

class Freebie(Base):
    __tablename__ = "freebies"

    id = Column(Integer(), primary_key=True)
    item_name = Column(String(), nullable=False)
    value = Column(Integer(), nullable=False)
    company_id = Column(Integer(), ForeignKey("companies.id"))
    dev_id = Column(Integer(), ForeignKey("devs.id"))

    def __repr__(self):
        return f"<Item_name {self.item_name}, Value {self.value}>"

    def print_details(self):
        #Returns a formatted string with freebie details.
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"