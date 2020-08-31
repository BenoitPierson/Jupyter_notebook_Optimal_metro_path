def index_station_on_line(line_name, station_name, dict_lines):
    index = dict_lines[line_name][0].loc[dict_lines[line_name][0] == station_name].index[0]
    return index


def neighbors(line_name, station_name, dict_lines):
    neighbors_list = list()
    
    index_station = index_station_on_line(line_name, station_name, dict_lines)
    
    if dict_lines[line_name].iloc[index_station - 1][0] != 'START':
        neighbors_list.append(dict_lines[line_name].iloc[index_station - 1][0])
    if dict_lines[line_name].iloc[index_station + 1][0] != 'STOP':
        neighbors_list.append(dict_lines[line_name].iloc[index_station + 1][0])
    
    return neighbors_list


def neighbors_dict_definition(df_station, dict_lines, lines):
    neighbors_dict = dict()
    
    for station in df_station['Station']:
        neighbors_dict[station] = dict()
        
        for i in range(1,6):
            line = df_station['Correspondance_' + str(i)].loc[df_station['Station'] == station].values[0]
            if line in lines:
                for neighbor in neighbors(line, station.upper(), dict_lines):
                    neighbors_dict[station][neighbor] = (1, line)
            
    return neighbors_dict

def trip_spec(df_station):
    start_station = str()
    end_station = str()

    print('-'*50 + '\n\t\tENTER YOUR TRIP ... \n' + '-'*50 + '\n')
    
    while start_station.upper() not in df_station['Station'].values:
        start_station = input('FROM : ')
        start_station = start_station.upper()
        
        if start_station not in df_station['Station'].values:
            first_char = start_station[0]
            print('\nNON-VALID NAME, VALID NAMES OF SHAPE \"' + first_char + '*\" LISTED BELOW : \n' + '-'*60)
            for station in df_station['Station'].values: 
                if station[0] == first_char: print(station)        
  
    while end_station.upper() not in df_station['Station'].values:
        end_station = input('TO : ')
        end_station = end_station.upper()
        
        if end_station not in df_station['Station'].values:
            first_char = end_station[0]
            print('\nNON-VALID NAME, VALID NAMES OF SHAPE \"' + first_char + '*\" LISTED BELOW : \n' + '-'*60)
            for station in df_station['Station'].values: 
                if station[0] == first_char: print(station)      
           
    return (start_station, end_station)

def is_labeled(labeled_vertices,vertex):
    return vertex in labeled_vertices

def add_to_labeled_vertices(labeled_vertices, vertex):
    labeled_vertices.append(vertex)

def heap_pop(heap):
    node, weight, line, parent = heap.pop(0)
    return (node, weight, line, parent)

def heap_add_or_replace(heap, triplet):    
    add=False
    if(len(heap)==0):
        heap.append(triplet)
    
    else:
        index=len(heap)
        for i in range(len(heap)):
            if(heap[i][0]==triplet[0]):
                
                if(heap[i][1]<=triplet[1]):
                    return 0
                else:
                    heap.pop(i)
                    if(add==False):
                        index=i
                    break
                        
            if(add==False):
                if(heap[i][1]>triplet[1]):
                    index=i
                    add=True
             
        heap.insert(index,triplet)

def Dijkstra(maze_graph, sourceNode):
    # Variable storing the labeled vertices nodes not to go there again
    labeled_vertices = list()
    
    # Stack of nodes
    heap = list()
    
    #Parent Dictionary
    parent_dict = dict()

    # Distances 
    distances = dict()
    
    # First call
    initial_tuple = (sourceNode, 0, -1, sourceNode)#Node to visit, distance from origin, parent
    heap_add_or_replace(heap, initial_tuple)
    
    while len(heap) > 0:
        (node, cost, line, parent) = heap_pop(heap)
        if not (is_labeled(labeled_vertices, node)):
            parent_dict[node] = parent
            add_to_labeled_vertices(labeled_vertices, node)
            distances[node] = cost
            for neighbor in maze_graph[node]:
                if not (is_labeled(labeled_vertices, neighbor)):
                    heap_add_or_replace(heap, (neighbor, cost + maze_graph[node][neighbor][0], maze_graph[node][neighbor][1], node))
    return labeled_vertices, parent_dict, distances

def create_walk_from_parents(parent_dict, source_node, end_node):
    route_node = list()
    next_node = end_node

    while next_node != source_node:
        route_node.append(next_node)
        next_node = parent_dict[next_node]

    return list(reversed(route_node))


def A_to_B(maze_graph,node_source,node_end):
    
    labeled_vertices,parent_dict,_ = Dijkstra(maze_graph,node_source)
    walk = create_walk_from_parents(end_node = node_end, source_node = node_source, parent_dict = parent_dict)
    return walk


def get_direction(start_station, end_station, line, dict_lines):
    direction = str()
    
    start_index = index_station_on_line(line, start_station, dict_lines)
    end_index = index_station_on_line(line, end_station, dict_lines)
    
    if (start_index - end_index) < 0:
        direction = dict_lines[line].iloc[-2][0]
    
    else:
        direction = dict_lines[line].iloc[1][0]
    
    return direction


def Path_instruction_printing(neighbors_dict, start_station, end_station, walk, dict_lines):
    print()
    print('-'*80 + '\n\tOPTIMAL PATH : '+ str(start_station) + '  -->  ' + str(end_station) + '\n' +'-'*80)
    print('START AT ' + str(start_station))

    current_station = start_station
    list_lines_portion = list()
    direction = str()
    for next_station in walk:
        list_lines_portion.append(neighbors_dict[current_station][next_station][1])
    
        if len(list_lines_portion) == 1:
            direction = get_direction(start_station=current_station, end_station=next_station, line=list_lines_portion[-1], dict_lines=dict_lines) 
            print('TAKE ' + str(list_lines_portion[-1]) + ' (DIRECTION : '+ direction + ')' + ' AT  ' + str(current_station))
    
        elif list_lines_portion[-1] != list_lines_portion[-2] : 
            direction = get_direction(start_station=current_station, end_station=next_station, line=list_lines_portion[-1], dict_lines=dict_lines) 
            print('TAKE ' + str(list_lines_portion[-1]) + ' (DIRECTION : '+ direction + ')' + ' AT  ' + str(current_station))

        current_station = next_station

    print('STOP AT ' + str(current_station))

dict_typo_ascii_art = {'alpha' : (25,25),
                       'speed' : (8,4)}

def ascii_art(str_2_print, typo, typo_dict):
    
    filename = 'alphabet_ascii_' + typo + '.txt'
    width_letter = dict_typo_ascii_art[typo][0]
    height_letter = dict_typo_ascii_art[typo][1]

    str_2_print = str_2_print.upper()
    
    with open(filename, 'r') as file:
        
        for i in range(height_letter):
            line = file.readline()
            
            for letter in str_2_print:
                index_letter =  ord(letter) - ord('A')
                print(line[index_letter * width_letter : index_letter * width_letter + width_letter], end = '')
                
            print()

def print_file(filename):
    f = open(filename, 'r')
    file_contents = f.read()
    print (file_contents)
    f.close()

def starting_menu():
    print('-'*125)
    ascii_art(str_2_print = 'metro', typo = 'alpha', typo_dict = dict_typo_ascii_art)
    print('\t\t\t\t\t... FIND YOUR PATH IN PARIS METRO ...\n\n')
    print_file(filename = 'intro.txt')
    print('\n\n')
