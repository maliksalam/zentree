import csv
import json
from collections import defaultdict

with open('data/masters.csv', encoding='ISO-8859-1') as f:
    data = csv.reader(f)
    data=list(data)

people = data[1:]

# construct list of parents
parents = defaultdict(list)
for p in people:
    parents[p[3]].append(p)

def buildtree(t=None, parent_eid='', gen=1):
    """
    Given a parents lookup structure, construct
    a data hierarchy.
    """
    parent = parents.get(parent_eid, None)
    if parent is None:
        return t
    for py_name, kr_name, jp_name, teacher, bio, birth_date, death_date, display_birth, display_death, works, links in parent:
        info_string_template = """<b>{py_name}</b> ({bd_dates})
        <br>{gen_ord} generation
        <br>Aliases: {other_names}
        <br><br>{bio}
        """
        works_string = "<br><br><b>Works:</b> <i>{works}</i>"
        
        if kr_name:
            other_names = ", ".join([jp_name, kr_name])
            all_names = " / ".join([py_name, jp_name, kr_name])
        else:
            other_names = jp_name
            all_names = " / ".join([py_name, jp_name])
        
        if not (birth_date or death_date):
            bd_dates = "n.d."
        elif not birth_date:
            bd_dates = "?-{}".format(death_date)
        elif not death_date:
            bd_dates = "{}-?".format(birth_date)
        else:
            bd_dates = "{}-{}".format(birth_date, death_date)
            
        gen_dict = {
            1: "1st",
            2:"2nd",
            3:"3rd",
            
                   }
        if gen <= 3:
            gen_ord = gen_dict[gen]
        else:
            gen_ord = str(gen)+'th'
            
        if works:
            info_string_template += works_string
            info_string = info_string_template.format(py_name=py_name, 
                                                      bd_dates = bd_dates,
                                                      gen_ord=gen_ord,
                                                      other_names=other_names, 
                                                      bio=bio, 
                                                      works=works)
        else:
            info_string = info_string_template.format(py_name=py_name, 
                                                      gen_ord=gen_ord,
                                                      bd_dates = bd_dates,
                                                      other_names=other_names, 
                                                      bio=bio)
            
        child = {
            'all_names': all_names,
            'py_name': py_name,
            'jp_name': jp_name,
            'dates': [display_birth, display_death],
            'info': info_string
                }
        if t is None:
            t = child
        else:
            children = t.setdefault('children', [])
            children.append(child)
            
        buildtree(child, py_name, gen+1)
    return t

data = buildtree(t=None, parent_eid='')

with open('data/lineage.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)