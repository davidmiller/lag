from django import template

register = template.Library()

JQUERY_TMPL = """
<script id="%s" type="text/x-jquery-tmpl">
  %s
</script>
"""

class TmplNode(template.Node):
    """
    Render a .tmpl partial as x-jquery-tmpl
    """

    def __init__(self, tmpl_path, selector):
        """
        Just drop variables to instance.

        Arguments:
        - `tmpl_path`:
        - `selector`:
        """
        self._tmpl_path = tmpl_path
        self._selector = selector

    def render(self, context):
        """
        Spit It Out

        Arguments:
        - `context`:
        """
        tpl = template.loader.get_template(self._tmpl_path)
        to_textnode = lambda x: template.TextNode("${%s}" % x.filter_expression.token)
        txtnodes = [n if isinstance(n, template.TextNode) else to_textnode(n) for n in tpl.nodelist]
        tpl.nodelist = template.NodeList(txtnodes)
        return JQUERY_TMPL % (self._selector, tpl.render(template.Context()))


@register.tag(name="tmpl")
def tmpl(parser, token):
    """
    Render a jQuery .tmpl fragment

    {% tmpl "fragment/path" "id" %}

    Arguments:
    - `parser`:
    - `token`:
    """
    try:
        tag, tmpl_path, selector = token.split_contents()
    except ValueError:
        msg = "%r tag requires 3 arguments" % token.contents.split()[0]
        raise template.TemplateSyntaxError(msg)
    return TmplNode(tmpl_path[1:-1], selector[1:-1])
