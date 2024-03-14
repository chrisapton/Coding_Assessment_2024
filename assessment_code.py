import json
import numpy as np
import pandas as pd

"""
Assuming that the team they are hiring for is for a technical team rather than a physically demanding team
Weighing intelligance positively, using strength and endurance as like diverse traits (further from team average, the better), 
spicyfoodtolorance trait would depend on the group, ex/ if everyone in the group tolorates 
spicy food, maybe hiring someone who can also have that too. 
"""

def score_applicants(input_data):
    team = input_data["team"]
    applicants = input_data["applicants"]

    # Attributes, assuming every applicant has the same attributes
    attributes = list(applicants[0]["attributes"].keys())

    # Getting team averages for each attribute
    average_attributes = [0] * len(attributes)
    for member in team:
        for attribute_ind in range(len(attributes)):
            average_attributes[attribute_ind] += member["attributes"][attributes[attribute_ind]]
    
    average_attributes = [i / len(team) for i in average_attributes]
    
    #print(attributes)
    #print(average_attributes)

    # Weight factors:
    intelligence_weight = 1.0
    strength_weight = 0.25
    endurance_weight = 0.25
    spicy_food_weight = 0.5

    scored_applicants = []
    for applicant in applicants:
        # Each attribute has a score between 1-10
        score = 0
        score += intelligence_weight * applicant["attributes"]["intelligence"] / 10

        # Scoring based on differences from average
        score += strength_weight * abs(applicant["attributes"]["strength"] - average_attributes[1]) / 10
        score += endurance_weight * abs(applicant["attributes"]["endurance"] - average_attributes[2]) / 10

        # Scoring based on similarity to average
        score += spicy_food_weight * (1 - abs(applicant["attributes"]["spicyFoodTolerance"] - average_attributes[3]) / 10)

        # Normalizing the score to be between [0,1]
        score = score / (intelligence_weight + strength_weight + endurance_weight + spicy_food_weight)
        score = round(score, 4)
        scored_applicants.append({'name': applicant['name'], 'score': score})
    
    # Saving the json object as output.json
    with open("output.json", "w") as outfile:
        json.dump({'scoredApplicants': scored_applicants}, outfile, indent=2)

    return scored_applicants

file = open('input.json')
data = json.load(file)

output = score_applicants(data)

print(output)
