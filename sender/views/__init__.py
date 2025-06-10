from .addressee import (AddresseeCreateView,   # noqa: F401
                        AddresseeUpdateView,   # noqa: F401
                        AddresseeDetailView,   # noqa: F401
                        AddresseeDeleteView,   # noqa: F401
                        AddresseeListView)     # noqa: F401

from .home import HomeView                     # noqa: F401
from .mailing import (MailingCreateView,       # noqa: F401
                      MailingListView,         # noqa: F401
                      MailingUpdateView,       # noqa: F401
                      MailingDetailView,       # noqa: F401
                      MailingDeleteView,       # noqa: F401
                      SendMailing,             # noqa: F401
                      StopMailingView)         # noqa: F401
from .message import (MessageCreateView,       # noqa: F401
                      MessageListView,         # noqa: F401
                      MessageDetailView,       # noqa: F401
                      MessageUpdateView,       # noqa: F401
                      MessageDeleteView)       # noqa: F401
