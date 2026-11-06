"""NoteBookmarks package API."""
from .registry import Bookmark,BookmarkRegistry,required_parameters
from .manager import BookmarkManager
from .templates import BookmarkTemplate
from .variables import resolve_variables,validate_variables
from .linked_tables import LinkedTable,LinkedTableRegistry
__all__=["Bookmark","BookmarkRegistry","required_parameters","BookmarkManager","BookmarkTemplate","resolve_variables","validate_variables","LinkedTable","LinkedTableRegistry"]
