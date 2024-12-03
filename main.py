message = """

"""

additional_prompt = ""

from importlib import reload
import autogen

from lib import agents
reload(agents)


groupchat = autogen.GroupChat(
    agents=[
        agents.user,
        agents.job_developer,
        agents.critic_agent,
    ],
    messages=[],
    max_round=10
)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=agents.gpt4_config)

res = agents.user.initiate_chat(
    manager,
    message=message
)


import re
import pandas as pd

filtered_items = [item for item in res.chat_history if item.get('name') == 'Job_Developer']

pattern = r'```\w*\n(.*?)```'
matches = re.findall(pattern, filtered_items[-1]['content'], re.DOTALL)

with open("./output/performers_and_jobs.csv", 'w') as file:
    file.write(matches[0])

performers_and_jobs = pd.read_csv("./output/performers_and_jobs.csv", delimiter=';', index_col=False)

performers_and_jobs


import pandas as pd

performers_and_jobs = pd.read_csv("./output/performers_and_jobs.csv", delimiter=';', index_col=False)

try:
    performers_and_jobs = performers_and_jobs.rename(columns={'Role': 'Job Performer'})
except:
    pass

all_performers_and_jobs = pd.read_csv("./output/all_performers_and_jobs.csv", delimiter=';', index_col=False)

all_performers_and_jobs = pd.concat([all_performers_and_jobs, performers_and_jobs], ignore_index=True)
all_performers_and_jobs = all_performers_and_jobs.sort_values(by=all_performers_and_jobs.columns[0])
all_performers_and_jobs.to_csv("./output/all_performers_and_jobs.csv", sep=';', index=False)

all_performers_and_jobs

import pandas as pd

performers_and_jobs = pd.read_csv("./output/all_performers_and_jobs.csv", delimiter=';', index_col=False)

message = f"""
Here the Job Performers list:
{';'.join(list(performers_and_jobs['Job Performer'].unique()))}
"""

from importlib import reload
import autogen

import lib.agents as agents
reload(agents)


groupchat = autogen.GroupChat(
    agents=[
        agents.user,
        agents.business_expert,
        agents.critic_agent,
    ],
    messages=[],
    max_round=10
)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=agents.gpt4_config)

res = agents.user.initiate_chat(
    manager,
    message=message
)

import re

filtered_items = [item for item in res.chat_history if item.get('name') == 'Business_Expert']

pattern = r'```\w*\n(.*?)```'
matches = re.findall(pattern, filtered_items[-1]['content'], re.DOTALL)

with open("./output/performers_scores.csv", 'w') as file:
    file.write(matches[0])

performers_scores = pd.read_csv("./output/performers_scores.csv", delimiter=';', index_col=False)

performers_scores.sort_values('Total Score',ascending=False)
selected_job_performers = ""
selected_main_job = ""
number = "5"
additional_prompt   = ""

from importlib import reload
import autogen

import lib.agents as agents
reload(agents)

groupchat = autogen.GroupChat(
    agents=[
        agents.user,
        agents.performer_generator,
        agents.critic_agent,
    ],
    messages=[],
    max_round=10
)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=agents.gpt4_config)

res = agents.user.initiate_chat(
    manager,
    message=f"""

Generate {number}

Job Performers: {selected_job_performers}
In which their Main Job is {selected_main_job}
"""
)

import re

filtered_items = [item for item in res.chat_history if item.get('name') == 'Performer_generator']

pattern = r'```\w*\n(.*?)```'
matches = re.findall(pattern, filtered_items[-1]['content'], re.DOTALL)

with open("./output/performers.csv", 'w') as file:
    file.write(matches[0])

performers = pd.read_csv("./output/performers.csv", delimiter=';', index_col=False)

performers

import pandas as pd

performers = pd.read_csv('./output/performers.csv',delimiter=';', index_col=False)

import json

from importlib import reload

import lib.interview_performers as agents

reload(agents)

interviews = []
for index, row in performers.iterrows():
    performer = row.to_json()

    main_job_related = f"""Answer the following question focusing and thinking about the main job {selected_main_job} applied to what you are doing as {row['Profession']}.
    If the main job {selected_main_job} is not related to you, simply answer \"This is not my main job\" and skip the question."""

    # main_job_related = ""

    res = agents.chain.invoke({"job_performer": performer, "main_job_related": main_job_related})
    res_dict = json.loads(res.additional_kwargs['function_call']['arguments'])

    interview = pd.DataFrame(res_dict["interview"])

    job_performer_dict = row.to_dict()

    job_performer_dict.update({"interview": interview})

    interviews.append(job_performer_dict)



import os
import json
import copy

outdir = './output/interviews'
if not os.path.exists(outdir):
    os.mkdir(outdir)

interviews_to_save = copy.deepcopy(interviews)

for interview in interviews_to_save:
    filename = os.path.join(outdir,"_".join((
        interview["Name"].replace(" ", ""),
        interview["Profession"].replace(" ", ""),
        ))+".json")

    interview["interview"] = interview["interview"].to_dict(orient='records')

    with open(filename, 'w') as json_file:
        json.dump(interview, json_file)

del interviews_to_save


import os
import json

outdir = './output/interviews'

# Initialize an empty list to store the data
interviews_to_analyze = []

# Loop through each file in the folder
for filename in os.listdir(outdir):
    if filename.endswith('.json'):
        file_path = os.path.join(outdir, filename)
        with open(file_path, 'r') as file:
            # Load the JSON data from the file
            json_data = json.load(file)
            # Append the data to the list
            interviews_to_analyze.append(json_data)


from importlib import reload
import autogen

import lib.agents as agents
reload(agents)

groupchat = autogen.GroupChat(
    agents=[
        agents.user,
        agents.jtbd_analyzer,
        agents.critic_agent,
    ],
    messages=[],
    max_round=10
)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=agents.gpt4_config)

res = agents.user.initiate_chat(
    manager,
    message=f"""
Analyse the following interviews using JTBD framework
{interviews_to_analyze}
"""
)

import re
import pandas as pd

filtered_items = [item for item in res.chat_history if item.get('name') == 'JTBD_Analyzer']

pattern = r'```\w*\n(.*?)```'
matches = re.findall(pattern, filtered_items[-1]['content'], re.DOTALL)

with open("./output/analysis.csv", 'w') as file:
    file.write(matches[0])

analysis = pd.read_csv("./output/analysis.csv", delimiter=';', index_col=False)

analysis

import pandas as pd

analysis = pd.read_csv("./output/analysis.csv", delimiter=';', index_col=False)

from importlib import reload
import autogen

import lib.agents as agents

reload(agents)

groupchat = autogen.GroupChat(
    agents=[
        agents.user,
        agents.critic_agent,
        agents.jtbd_categorizer,
    ],
    messages=[],
    max_round=10
)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=agents.gpt4_config)

res = agents.user.initiate_chat(
    manager,
    message=f"""

The main job is {selected_main_job} while the steps are:

{analysis}

"""
)

import re

filtered_items = [item for item in res.chat_history if item.get('name') == 'JTBD_Categorizer']

pattern = r'```\w*\n(.*?)```'
matches = re.findall(pattern, filtered_items[-1]['content'], re.DOTALL)

with open("./output/category.csv", 'w') as file:
    file.write(matches[0])

category = pd.read_csv("./output/category.csv", delimiter=';', index_col=False)

custom_order = [
    'Define',
    'Locate',
    'Prepare',
    'Confirm',
    'Execute',
    'Monitor',
    'Modify',
    'Conclude'
]

category['Category'] = pd.Categorical(category['Category'], categories=custom_order, ordered=True)
category_sorted = category.sort_values('Category').reset_index(drop=True)

category_sorted.to_csv("./output/category.csv", sep=';')

import pandas as pd

category_sorted = pd.read_csv("./output/category.csv", delimiter=';', index_col=False)
category_sorted




from importlib import reload
import autogen

import lib.agents as agents

reload(agents)

groupchat = autogen.GroupChat(
    agents=[
        agents.user,
        agents.planner,
        agents.solution_generator,
        agents.digital_product_designer,
        agents.critic_agent,
    ],
    messages=[],
    max_round=10
)


manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=agents.gpt4_config)

res = agents.user.initiate_chat(
    manager,
    message=f"""

We run a Jobs-to-be-done Analysis. Here the information:

Job Performer: {selected_job_performers}

Main Jobs: {selected_main_job}

Job Steps and Needs:
{category_sorted[["Job Step", "Need"]]}
"""
)

import re
import json

filtered_items = [item for item in res.chat_history if item.get('name') == 'Digital_Product_Designer']

pattern = r'```json\n(.*?)```'
matches = re.findall(pattern, filtered_items[-1]['content'], re.DOTALL)


solutions = json.loads(matches[0])[0]

with open("./output/solutions.json", 'w') as file:
    json.dump(solutions, file, indent=4)


import json

with open("./output/solutions.json") as file:
    solutions = json.load(file)



from importlib import reload
import autogen

import lib.agents as agents

reload(agents)

groupchat = autogen.GroupChat(
    agents=[
        agents.user,
        agents.storybrand_expert,
        agents.critic_agent,
        agents.copywriting_expert
    ],
    messages=[],
    max_round=10
)


manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=agents.gpt4_config)

res = agents.user.initiate_chat(
    manager,
    message=f"""

Here the document describing the solutions and the problem that comes from JTBD.

{solutions}
"""
)



