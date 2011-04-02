from django.shortcuts import render_to_response
from django.template import RequestContext

def render_to(template):
    """
    Decorator that wraps render_to_response and provides a nicer syntax for
    using the shortcut for a majority of views while not having to explicitly
    add the request context.

    Will render to template.
    the wrapped view function should return either a dictionary to be passed
    or whatever response will just be passed up the stack as is.
    """
    def renderer(view):
        "Takes the view"
        def _apply_context(request, *args, **kwargs):
            """
            Either pass output up the stack, or render_to_response, adding
            RequestContext() as we go
            """
            output = view(request, *args, **kwargs)
            if not isinstance(output, dict):
                return output
            context = RequestContext(request)
            print template
            return render_to_response(template,
                                      output,
                                      context_instance=context)
        return _apply_context
    return renderer
