"""
This type stub file was generated by pyright.
"""

from typing import Optional

"""sys.excepthook for IPython itself, leaves a detailed report on disk.

Authors:

* Fernando Perez
* Brian E. Granger
"""
_default_message_template = ...
_lite_message_template = ...
class CrashHandler:
    """Customizable crash handlers for IPython applications.

    Instances of this class provide a :meth:`__call__` method which can be
    used as a ``sys.excepthook``.  The :meth:`__call__` signature is::

        def __call__(self, etype, evalue, etb)
    """
    message_template = ...
    section_sep = ...
    def __init__(self, app, contact_name: Optional[str] = ..., contact_email: Optional[str] = ..., bug_tracker: Optional[str] = ..., show_crash_traceback: bool = ..., call_pdb: bool = ...) -> None:
        """Create a new crash handler

        Parameters
        ----------
        app : Application
            A running :class:`Application` instance, which will be queried at
            crash time for internal information.
        contact_name : str
            A string with the name of the person to contact.
        contact_email : str
            A string with the email address of the contact.
        bug_tracker : str
            A string with the URL for your project's bug tracker.
        show_crash_traceback : bool
            If false, don't print the crash traceback on stderr, only generate
            the on-disk report
        call_pdb
            Whether to call pdb on crash

        Attributes
        ----------
        These instances contain some non-argument attributes which allow for
        further customization of the crash handler's behavior. Please see the
        source for further details.

        """
        ...
    
    def __call__(self, etype, evalue, etb): # -> None:
        """Handle an exception, call for compatible with sys.excepthook"""
        ...
    
    def make_report(self, traceback):
        """Return a string containing a crash report."""
        ...
    


def crash_handler_lite(etype, evalue, tb): # -> None:
    """a light excepthook, adding a small message to the usual traceback"""
    ...
