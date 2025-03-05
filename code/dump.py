import json, os

# =============================================================================
# region positions
# =============================================================================

positions = {
    "home" : [1.3348536491394043, -1.6144734821715296, 1.5730488936053675, -1.5615404548919578, -1.5539191404925745, -0.2927349249469202],
    "pickup": [
    [1.0654441118240356, -1.219952182178833, 1.8635318914996546, -2.2141744099059046, -1.5864689985858362, -0.29245120683778936] , # 0
    [1.0669639110565186, -1.171164945965149, 1.791931454335348, -2.179608007470602, -1.5372656027423304, -0.48901683488954717], # 1
    [1.0893298387527466, -1.1207396549037476, 1.7084930578814905, -2.1476899586119593, -1.5345671812640589, 1.062324047088623] , # 2
    [1.114319086074829, -1.1392197769931336, 1.7042668501483362, -2.1286589107909144, -1.5964182058917444, 1.5022380352020264] #3
    # , [1.108981728553772, -1.2619552177241822, 1.9085477034198206, -2.203841825524801, -1.5254181067096155, 1.0677990913391113] # 4
    # , [1.1437020301818848, -1.2171921294978638, 1.85162860551943, -2.2235738239684046, -1.5547211805926722, 1.8110084533691406] # 5
    # , [1.1509544849395752, -1.1585918825915833, 1.7517932097064417, -2.1524983845152796, -1.526743237172262, 1.8083500862121582] # 6
    # , vial_pickup_0 = [1.177856206893921, -1.1080926221660157, 1.682671372090475, -2.15537752727651, -1.541666332875387, 1.8952510356903076] # 7
    ],
    "VP_interm" : [1.1170587539672852, -1.4987735611251374, 1.561568562184469, -1.6459490261473597, -1.552575413380758, 1.0632418394088745],
    "stir_interm" : [1.3532801866531372, -1.5073005569032212, 1.868021313344137, -1.9257518253722132, -1.5573704878436487, -0.2886012236224573],
    "stirer" :  [1.353271722793579, -1.4905654725483437, 1.9034879843341272, -1.9808117351927699, -1.5576022307025355, -0.2884419600116175],
    "camera" : [1.5405631065368652, -1.9327041111388148, 2.2914238611804407, -1.9269162617125453, -1.5510247389422815, -0.29272157350649053],
    "end_interm" : [
    [1.6904239654541016, -1.160712794666626, 1.7000702063189905, -2.10415043453359, -1.571395222340719, -0.2879074255572718] # 1
    , [1.6643126010894775, -1.1203327637961884, 1.644454304371969, -2.10503687481069, -1.52537709871401, 0.014248140156269073] # 2
    , [1.683838963508606, -1.0438754719546814, 1.5111497084247034, -2.0103875599303187, -1.5697210470782679, -0.28976756731142217] # 3
    , [1.668087124824524, -1.0212004345706482, 1.4788315931903284, -2.0429655514159144, -1.541999642048971, -0.29016143480409795] # 4
    ],
    "end" : [
    [1.6904000043869019, -1.130103514795639, 1.7256429831134241, -2.1604229412474574, -1.5716236273394983, -0.287788216267721] # 1
    , [1.664297103881836, -1.09848044932399, 1.6634991804706019, -2.1458922825255335, -1.5255277792560022, 0.014332280494272709] # End_2
    , [1.683842420578003, -1.0204988282969971, 1.533896271382467, -2.0565110645689906, -1.569904629384176, -0.2896679083453577] # End_3
    , [1.6784923076629639, -0.9912229341319581, 1.4889605681048792, -2.076402326623434, -1.5669849554644983, 4.669535160064697] # End_4
    ] 
}

# =============================================================================
# region Dump
# =============================================================================

def dump(positions):
    """ Saves the `positions` dictionary into a JSON file named 'positions.json' in the current directory """

    # Finds/Makes data dir in current dir and saves file path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    file_name = "positions.json"
    file_path = os.path.join(data_dir, file_name)

    # Write the positions dictionary to a JSON file
    with open(file_path, "w") as file:
        json.dump(positions, file, indent=4)

# =============================================================================
# region Main
# =============================================================================

if __name__ == '__main__':
    dump(positions)
