from Base import Base
from sqlalchemy import Column, String, Integer
from constants import MAX_LENGTH
# Table for the democrat table in database
# for ORM
class Democrat(Base):
    __tablename__ = 'democrat'
    id = Column(Integer, primary_key=True)
    q1 = Column(String(MAX_LENGTH))
    q2 = Column(String(MAX_LENGTH))
    q3 = Column(String(MAX_LENGTH))
    q4 = Column(String(MAX_LENGTH))
    q5 = Column(String(MAX_LENGTH))
    q6 = Column(String(MAX_LENGTH))
    q7 = Column(String(MAX_LENGTH))
    q8 = Column(String(MAX_LENGTH))
    q9 = Column(String(MAX_LENGTH))
    q10 = Column(String(MAX_LENGTH))
    q11 = Column(String(MAX_LENGTH))
    q12 = Column(String(MAX_LENGTH))
    q13 = Column(String(MAX_LENGTH))
    q14 = Column(String(MAX_LENGTH))
    q15 = Column(String(MAX_LENGTH))
    def __init__(self,*kwargs):
        self.q1 = kwargs[0]
        self.q2 = kwargs[1]
        self.q3 = kwargs[2]
        self.q4 = kwargs[3]
        self.q5 = kwargs[4]
        self.q6 = kwargs[5]
        self.q7 = kwargs[6]
        self.q8 = kwargs[7]
        self.q9 = kwargs[8]
        self.q10 = kwargs[9]
        self.q11 = kwargs[10]
        self.q12 = kwargs[11]
        self.q13 = kwargs[12]
        self.q14 = kwargs[13]
        self.q15 = kwargs[14]