import os
from random import choice

try:
    import ujson
except ImportError:
    import json as ujson

class Thoughts():
    def __init__(self,
                 id,
                 biome=None,
                 season=None,
                 thoughts=None,
                 has_injuries=None,
                 perm_conditions=None,
                 relationship_constraint=None,
                 main_backstory_constraint=None,
                 random_backstory_constraint=None,
                 main_status_constraint=None,
                 random_status_constraint=None,
                 main_age_constraint=None,
                 random_age_constraint=None,
                 main_trait_constraint=None,
                 random_trait_constraint=None,
                 main_skill_constraint=None,
                 random_skill_constraint=None):
        self.id = id
        self.biome = biome if biome else ["Any"]
        self.season = season if season else ["Any"]

        if thoughts:
            self.thoughts = thoughts
        else:
            self.thoughts = [f"Isn't thinking about much at the moment"]
        
        if has_injuries: # for if a cat has injuries
            self.has_injuries = has_injuries
        else:
            self.has_injuries = {}
        
        if perm_conditions: # for a cat with a perm condition
            self.perm_conditions = perm_conditions
        else:
            self.perm_conditions = []
        
        if relationship_constraint: # handles relationships such as sibling, parents, etc
            self.relationship_constraint = relationship_constraint
        else:
            self.relationship_constraint = []
        
        if main_backstory_constraint: # if backstory of the mc must be specific
            self.main_backstory_constraint = main_backstory_constraint
        else:
            self.main_backstory_constraint = {}

        if random_backstory_constraint: # if backstory of the rc must be specific
            self.random_backstory_constraint = random_backstory_constraint
        else:
            self.random_backstory_constraint = {}

        if main_status_constraint: 
            self.main_status_constraint = main_status_constraint
        else:
            self.main_status_constraint = []

        if random_status_constraint:
            self.random_status_constraint = random_status_constraint
        else:
            self.random_status_constraint = []

        if main_age_constraint:
            self.main_age_constraint = main_age_constraint
        else:
            self.main_age_constraint = []

        if random_age_constraint:
            self.random_age_constraint = random_age_constraint
        else:
            self.random_age_constraint = []

        if main_trait_constraint:
            self.main_trait_constraint = main_trait_constraint
        else:
            self.main_trait_constraint = []

        if random_trait_constraint:
            self.random_trait_constraint = random_trait_constraint
        else:
            self.random_trait_constraint = []

        if main_skill_constraint:
            self.main_skill_constraint = main_skill_constraint
        else:
            self.main_skill_constraint = []

        if random_skill_constraint:
            self.random_skill_constraint = random_skill_constraint
        else:
            self.random_skill_constraint = []

# ---------------------------------------------------------------------------- #
#                some useful functions, related to thoughts                    #
# ---------------------------------------------------------------------------- #

def thought_fulfill_rel_constraints(relationship, constraint, thought_id) -> bool:
    """Check if the relationship fulfills the interaction relationship constraints."""
    # if the constraints are not existing, they are considered to be fulfilled
    if not constraint:
        return True
    if len(constraint) == 0:
        return True
            
    if "siblings" in constraint and not relationship.cat_from.is_sibling(relationship.cat_to):
        return False

    if "mates" in constraint and not relationship.mates:
        return False

    if "not_mates" in constraint and relationship.mates:
        return False

    if "parent/child" in constraint and not relationship.cat_from.is_parent(relationship.cat_to):
        return False

    if "child/parent" in constraint and not relationship.cat_to.is_parent(relationship.cat_from):
        return False

    return True

def cats_fulfill_thought_constraints(main_cat, random_cat, thought, game_mode) -> bool:
    """Check if the two cats fulfills the thought constraints."""
    if len(thought.relationship_constraint) >= 1:
        for constraint in thought.relationship_constraint:
            if thought_fulfill_rel_constraints(main_cat, constraint, thought.id):
                continue

    if len(thought.main_status_constraint) >= 1:
        if main_cat.status not in thought.main_status_constraint:
            return False

    if len(thought.random_status_constraint) >= 1:
        if random_cat.status not in thought.random_status_constraint:
            return False
        
    if len(thought.main_age_constraint) >= 1:
        if main_cat.age not in thought.main_age_constraint:
            return False

    if len(thought.random_age_constraint) >= 1:
        if random_cat.age not in thought.random_age_constraint:
            return False

    if len(thought.main_trait_constraint) >= 1:
        if main_cat.trait not in thought.main_trait_constraint:
            return False

    if len(thought.random_trait_constraint) >= 1:
        if random_cat.trait not in thought.random_trait_constraint:
            return False

    if len(thought.main_skill_constraint) >= 1:
        if main_cat.skill not in thought.main_skill_constraint:
            return False

    if len(thought.random_skill_constraint) >= 1:
        if random_cat.skill not in thought.random_skill_constraint:
            return False

    if len(thought.main_backstory_constraint) >= 1:
        if "m_c" in thought.main_backstory_constraint:
            if main_cat.backstory not in thought.main_backstory_constraint["m_c"]:
                return False
            
    if len(thought.random_backstory_constraint) >= 1:
        if "r_c" in thought.random_backstory_constraint:
            if random_cat.backstory not in thought.random_backstory_constraint["r_c"]:
                return False

    if len(thought.has_injuries) >= 1:
        # if there is a injury constraint and the clan is in classic mode, this interact can not be used
        if game_mode == "classic":
            return False

        if "m_c" in thought.has_injuries:
            injuries_in_needed = list(
                filter(lambda inj: inj in thought.has_injuries["m_c"], main_cat.injuries.keys())
            )
            if len(injuries_in_needed) <= 0:
                return False
        if "r_c" in thought.has_injuries:
            injuries_in_needed = list(
                filter(lambda inj: inj in thought.has_injuries["r_c"], random_cat.injuries.keys())
            )
            if len(injuries_in_needed) <= 0:
                return False

    return True
# ---------------------------------------------------------------------------- #
#                            BUILD MASTER DICTIONARY                           #
# ---------------------------------------------------------------------------- #

def create_thoughts(inter_list) -> list:
    created_list = []
    for inter in inter_list:
        created_list.append(Thoughts(
            id=inter["id"],
            biome=inter["biome"] if "biome" in inter else ["Any"],
            season=inter["season"] if "season" in inter else ["Any"],
            thoughts=inter["thoughts"] if "thoughts" in inter else None,
            has_injuries=inter["has_injuries"] if "has_injuries" in inter else None,
            perm_conditions=inter["perm_conditions"] if "perm_conditions" in inter else None,
            relationship_constraint = inter["relationship_constraint"] if "relationship_constraint" in inter else None,
            main_backstory_constraint = inter["main_backstory_constraint"] if "main_backstory_constraint" in inter else None,
            random_backstory_constraint = inter["random_backstory_constraint"] if "random_backstory_constraint" in inter else None,
            main_status_constraint = inter["main_status_constraint"] if "main_status_constraint" in inter else None,
            random_status_constraint = inter["random_status_constraint"] if "random_status_constraint" in inter else None,
            main_age_constraint = inter["main_age_constraint"] if "main_age_constraint" in inter else None,
            random_age_constraint = inter["random_age_constraint"] if "random_age_constraint" in inter else None,
            main_trait_constraint = inter["main_trait_constraint"] if "main_trait_constraint" in inter else None,
            random_trait_constraint = inter["random_trait_constraint"] if "random_trait_constraint" in inter else None,
            main_skill_constraint = inter["main_skill_constraint"] if "main_skill_constraint" in inter else None,
            random_skill_constraint = inter["random_skill_constraint"] if "random_skill_constraint" in inter else None
        ))
    return created_list

def load_thoughts(main_cat, other_cat, age):
    base_path = os.path.join("resources", "dicts", "thoughts")
    life_dir = None
    thoughts = []

    if not main_cat.dead and not main_cat.outside:
        life_dir = "alive"
    elif not main_cat.dead and main_cat.outside:
        life_dir = "alive_outside"
    elif main_cat.dead and not main_cat.outside and not main_cat.df:
        life_dir = "starclan"
    elif main_cat.dead and not main_cat.outside and main_cat.df:
        life_dir = "darkforest"
    elif main_cat.dead and main_cat.outside:
        life_dir = "unknownresidence"

    THOUGHTS = []
    with open(os.path.join(base_path, life_dir, age, "general.json"), 'r') as read_file:
        THOUGHTS = ujson.loads(read_file.read())
    with open(os.path.join(base_path, life_dir, "general", "general.json"), 'r') as read_file:
        THOUGHTS += ujson.loads(read_file.read())

    thoughts = create_thoughts(THOUGHTS)
    return thoughts