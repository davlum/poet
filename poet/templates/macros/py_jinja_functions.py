from poet.models.entity import Entity
from markupsafe import Markup


def render_name_link(entity_id):
    entity = Entity.objects.get(pk=entity_id)
    names_ls = [entity.full_name, entity.alt_name]
    names_ls = ' - '.join([x for x in names_ls if x is not None])
    link = """<a href="/entity/%s"}}>%s</a>""" % (entity_id, names_ls)
    return Markup(link)
