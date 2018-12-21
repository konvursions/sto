"""Attach SQLAlchemy models to their "Base"

The framework user may supply their own base class e.g. for the case of fine tuning some database options.
Here we supply implementations for the default command line application using SQLite.
"""

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

from sto.models.utils import TimeStampedBaseModel
from .broadcastaccount import _BroadcastAccount, _PreparedTransaction
from .tokenscan import _TokenScanStatus, _TokenHolderDelta, _TokenHolderLastBalance


Base = declarative_base()


#
# We have split up models to two separate files without base to ensure they can reused across different Python projects
#

class BroadcastAccount(_BroadcastAccount, Base):
    pass

class PreparedTransaction(_PreparedTransaction, Base):

    broadcast_account_id = sa.Column(sa.ForeignKey("broadcast_account.id"), nullable=True)
    broadcast_account = orm.relationship(BroadcastAccount,
                        backref=orm.backref("txs",
                                        lazy="dynamic",
                                        cascade="all, delete-orphan",
                                        single_parent=True, ), )



class TokenScanStatus(_TokenScanStatus, Base):
    pass


class _TokenHolderDelta(_TokenHolderStatus, Base):

    token_id = sa.Column(sa.ForeignKey("token_scan_status.id"), nullable=True)
    token = orm.relationship(TokenScanStatus,
                        backref=orm.backref("holder_deltas",
                                        lazy="dynamic",
                                        cascade="all, delete-orphan",
                                        single_parent=True, ), )


class _TokenHolderLastBalance(_TokenHolderLastBalance, Base):

    token_id = sa.Column(sa.ForeignKey("token_scan_status.id"), nullable=True)
    token = orm.relationship(TokenScanStatus,
                        backref=orm.backref("balances",
                                        lazy="dynamic",
                                        cascade="all, delete-orphan",
                                        single_parent=True, ), )
