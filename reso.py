from sqlalchemy import Column, UnicodeText
from sqlalchemy_json import MutableJson, NestedMutableJson

from . import BASE, SESSION, engine
from sqlalchemy import Column, Numeric

from . import BASE, SESSION, engine


class NOLogPMs(BASE):
    __tablename__ = "no_log_pms"
    chat_id = Column(Numeric, primary_key=True)

    def __init__(self, chat_id, reason=""):
        self.chat_id = chat_id


NOLogPMs.__table__.create(bind=engine, checkfirst=True)


def is_approved(chat_id):
    try:
        return SESSION.query(NOLogPMs).filter(NOLogPMs.chat_id == chat_id).one()
    except BaseException:
        return None
    finally:
        SESSION.close()


def approve(chat_id):
    adder = NOLogPMs(chat_id)
    SESSION.add(adder)
    SESSION.commit()

def disapprove(chat_id):
    rem = SESSION.query(NOLogPMs).get(chat_id)
    if rem:
        SESSION.delete(rem)
        SESSION.commit()

class Cat_GlobalCollection_Json(BASE):
    __tablename__ = "cat_globalcollectionjson"
    keywoard = Column(UnicodeText, primary_key=True)
    json = Column(MutableJson)
    njson = Column(NestedMutableJson)

    def __init__(self, keywoard, json, njson):
        self.keywoard = keywoard
        self.json = json
        self.njson = njson


Cat_GlobalCollection_Json.__table__.create(bind=engine, checkfirst=True)


def get_collection(keywoard):
    try:
        return SESSION.query(Cat_GlobalCollection_Json).get(keywoard)
    finally:
        SESSION.close()


def add_collection(keywoard, json, njson=None):
    if njson is None:
        njson = {}
    to_check = get_collection(keywoard)
    if to_check:
        keyword_items = SESSION.query(Cat_GlobalCollection_Json).get(keywoard)
        SESSION.delete(keyword_items)
    keyword_items = Cat_GlobalCollection_Json(keywoard, json, njson)
    SESSION.add(keyword_items)
    SESSION.commit()
    return True


def del_collection(keywoard):
    to_check = get_collection(keywoard)
    if not to_check:
        return False
    keyword_items = SESSION.query(Cat_GlobalCollection_Json).get(keywoard)
    SESSION.delete(keyword_items)
    SESSION.commit()
    return True


def get_collections():
    try:
        return SESSION.query(Cat_GlobalCollection_Json).all()
    finally:
        SESSION.close()
