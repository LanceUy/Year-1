"""Assignment 2 functions."""

from typing import List


THREE_BY_THREE = [[1, 2, 1],
                  [4, 6, 5],
                  [7, 8, 9]]

FOUR_BY_FOUR = [[1, 2, 6, 5],
                [4, 5, 3, 2],
                [7, 9, 8, 1],
                [1, 2, 1, 4]]

UNIQUE_3X3 = [[1, 2, 3],
              [9, 8, 7],
              [4, 5, 6]]

UNIQUE_4X4 = [[10, 2, 3, 30],
              [9, 8, 7, 11],
              [4, 5, 6, 12],
              [13, 14, 15, 16]]

def compare_elevations_within_row(elevation_map: List[List[int]], map_row: int, 
                                  level: int) -> List[int]:
    """Return a new list containing the three counts: the number of
    elevations from row number map_row of elevation map elevation_map
    that are less than, equal to, and greater than elevation level.

    Precondition: elevation_map is a valid elevation map.
                  0 <= map_row < len(elevation_map).

    >>> compare_elevations_within_row(THREE_BY_THREE, 1, 5)
    [1, 1, 1]
    >>> compare_elevations_within_row(FOUR_BY_FOUR, 1, 2)
    [0, 1, 3]

    """
    within_row = elevation_map[map_row]
    new_list = []
    count_less = 0
    count_equal = 0
    count_more = 0
    
    for number in within_row:
        if number < level:
            count_less += 1
        elif number == level:
            count_equal += 1
        else:
            count_more += 1
    
    new_list.extend([count_less, count_equal, count_more])
    
    return new_list
            

def update_elevation(elevation_map: List[List[int]], start: List[int], 
                     stop: List[int], delta: int) -> None:
    """Modify elevation map elevation_map so that the elevation of each
    cell between cells start and stop, inclusive, changes by amount
    delta.

    Precondition: elevation_map is a valid elevation map.
                  start and stop are valid cells in elevation_map.
                  start and stop are in the same row or column or both.
                  If start and stop are in the same row,
                      start's column <=  stop's column.
                  If start and stop are in the same column,
                      start's row <=  stop's row.
                  elevation_map[i, j] + delta >= 1
                      for each cell [i, j] that will change.

    >>> THREE_BY_THREE_COPY = [[1, 2, 1],
    ...                        [4, 6, 5],
    ...                        [7, 8, 9]]
    >>> update_elevation(THREE_BY_THREE_COPY, [1, 0], [1, 1], -2)
    >>> THREE_BY_THREE_COPY
    [[1, 2, 1], [2, 4, 5], [7, 8, 9]]
    >>> FOUR_BY_FOUR_COPY = [[1, 2, 6, 5],
    ...                      [4, 5, 3, 2],
    ...                      [7, 9, 8, 1],
    ...                      [1, 2, 1, 4]]
    >>> update_elevation(FOUR_BY_FOUR_COPY, [1, 2], [3, 2], 1)
    >>> FOUR_BY_FOUR_COPY
    [[1, 2, 6, 5], 
     [4, 5, 4, 2], 
     [7, 9, 9, 1], 
     [1, 2, 2, 4]]

    """
    same_row = bool(start[0] == stop[0])
    same_column = bool(start[-1] == stop[-1])
    
    if same_row and not same_column: #mutate the values in row
        for i in range(start[-1], stop[-1] + 1):
            elevation_map[start[0]][i] += delta
    elif same_column and not same_row:
        for i in range(start[0], stop[0] + 1):
            elevation_map[i][start[-1]] += delta
    else:
        elevation_map[start[0]][start[-1]] += delta
    #return elevation_map    
        
def get_average_elevation(elevation_map: List[List[int]]) -> float:
    """Return the average elevation across all cells in the elevation map
    elevation_map.

    Precondition: elevation_map is a valid elevation map.

    >>> get_average_elevation(UNIQUE_3X3)
    5.0
    >>> get_average_elevation(FOUR_BY_FOUR)
    3.8125
    """
    total_sum = 0
    count = 0
    for sublist in elevation_map:
        for number in sublist:
            total_sum += number
            count += 1
    return total_sum/count

def find_peak(elevation_map: List[List[int]]) -> List[int]:
    """Return the cell that is the highest point in the elevation map
    elevation_map.

    Precondition: elevation_map is a valid elevation map.
                  Every elevation value in elevation_map is unique.

    >>> find_peak(UNIQUE_3X3)
    [1, 0]
    >>> find_peak(UNIQUE_4X4)
    [0, 3]
    """
    new_list = []
    largest = 0
    row = 0
    index = 0
            
    for i in range(len(elevation_map)):
        for j in range(len(elevation_map[i])):
            if elevation_map[i][j] > largest:
                largest = elevation_map[i][j]
                row = i
                index = j
    
    new_list.extend([row, index])
    return new_list

def is_sink(elevation_map: List[List[int]], cell: List[int]) -> bool:
    """Return True if and only if cell exists in the elevation map
    elevation_map and cell is a sink.

    Precondition: elevation_map is a valid elevation map.
                  cell is a 2-element list.

    >>> is_sink(THREE_BY_THREE, [0, 5])
    False
    >>> is_sink(THREE_BY_THREE, [0, 2])
    True
    >>> is_sink(THREE_BY_THREE, [1, 1])
    False
    >>> is_sink(FOUR_BY_FOUR, [2, 3])
    True
    >>> is_sink(FOUR_BY_FOUR, [3, 2])
    True
    >>> is_sink(FOUR_BY_FOUR, [1, 3])
    False
    """
    rows = len(elevation_map)
    cols = len(elevation_map[0]) if rows else 0    
    row_len = rows - 1
    col_len = cols - 1
    
    if cell[0] > row_len or cell[1] > col_len:
        return False
    
    for i in range(max(0, cell[0] - 1), min(rows, cell[0] + 2)):
        for j in range(max(0, cell[1] - 1), min(cols, cell[1] + 2)):
            if [i, j] != cell and elevation_map[cell[0]][cell[1]] > \
            elevation_map[i][j]:
                #print(elevation_map[i][j]) 
                return False
                   
    return True

def find_local_sink(elevation_map: List[List[int]],
                    cell: List[int]) -> List[int]:
    """Return the local sink of cell cell in elevation map elevation_map.

    Precondition: elevation_map is a valid elevation map.
                  elevation_map contains no duplicate elevation values.
                  cell is a valid cell in elevation_map.

    >>> find_local_sink(UNIQUE_3X3, [1, 1])
    [0, 0]
    >>> find_local_sink(UNIQUE_3X3, [2, 0])
    [2, 0]
    >>> find_local_sink(UNIQUE_4X4, [1, 3])
    [0, 2]
    >>> find_local_sink(UNIQUE_4X4, [2, 2])
    [2, 1]
    """
    new_list = []
    sub_list = []
    smallest = 0
    k = 0
    rows = len(elevation_map)
    cols = len(elevation_map[0]) if rows else 0    

    for i in range(max(0, cell[0] - 1), min(rows, cell[0] + 2)):
        for j in range(max(0, cell[1] - 1), min(cols, cell[1] + 2)):
            if [i, j] != cell: 
                #print(elevation_map[i][j]) 
                new_list.append([i, j])
                
    #print(new_list)
    """
    for j in range(len(new_list)):
        sub_list.append([elevation_map[new_list[j][0]][new_list[j][1]]])
    """
    while k < len(new_list):
        sub_list.append([elevation_map[new_list[k][0]][new_list[k][1]]]) 
        k += 1

    #print(sub_list)
    smallest = min(sub_list)  
    index1 = sub_list.index(smallest)
    #print(index1)
    
    return new_list[index1]  

def can_hike_to(elevation_map: List[List[int]], start: List[int],
                dest: List[int], supplies: int) -> bool:
    """Return True if and only if a hiker can go from start to dest in
    elevation_map without running out of supplies.

    Precondition: elevation_map is a valid elevation map.
                  start and dest are valid cells in elevation_map.
                  dest is North-West of start.
                  supplies >= 0

    >>> map = [[1, 6, 5, 6],
    ...        [2, 5, 6, 8],
    ...        [7, 2, 8, 1],
    ...        [4, 4, 7, 3]]
    >>> can_hike_to(map1, [3, 3], [2, 2], 10)
    True
    >>> can_hike_to(map1, [3, 3], [2, 2], 8)
    False
    >>> can_hike_to(map1, [3, 3], [3, 0], 7)
    True
    >>> can_hike_to(map1, [3, 3], [3, 0], 6)
    False
    >>> can_hike_to(map1, [3, 3], [0, 0], 18)
    True
    >>> can_hike_to(map1, [3, 3], [0, 0], 17)
    False

    """
    tot = 0

    while start != dest:
        if start[0] == dest[0]: #same row
           # direction = west
            tot += abs(elevation_map[start[0]][start[1]] - \
                       elevation_map[start[0]][start[1] - 1])
            start = [start[0], start[1] - 1]          
        elif start[1] == dest[1]: #same column
            # direction = north
            tot += abs(elevation_map[start[0]][start[1]] - \
                       elevation_map[start[0]-1][start[1]])
            start = [start[0]-1, start[1]]   
        else:
            totx = abs(elevation_map[start[0]][start[1]] - \
                       elevation_map[start[0]][start[1] - 1])
            toty = abs(elevation_map[start[0]][start[1]] - \
                       elevation_map[start[0]-1][start[1]])
            if totx >= toty:
                tot += toty
                start = [start[0]-1, start[1]] 
            else:
                tot += totx
                start = [start[0], start[1] - 1]
                
    return tot <= supplies
    
def get_lower_resolution(elevation_map: List[List[int]]) -> List[List[int]]:
    """Return a new elevation map, which is constructed from the values
    of elevation_map by decreasing the number of elevation points
    within it.

    Precondition: elevation_map is a valid elevation map.

    >>> get_lower_resolution(
    ...     [[1, 6, 5, 6],
    ...      [2, 5, 6, 8],
    ...      [7, 2, 8, 1],
    ...      [4, 4, 7, 3]])
    [[3, 6], [4, 4]]
    >>> get_lower_resolution(
    ...     [[7, 9, 1],
    ...      [4, 2, 1],
    ...      [3, 2, 3]])
    [[5, 1], [2, 3]]

    """
    sub_list = []
    final_list = []
    comon = []
    rows = len(elevation_map)
    cols = len(elevation_map[0]) if rows else 0    

    # Group values by 2x2 or smaller formations
    for a in range(0, rows, 2):
        for b in range(0, cols, 2):
            new_list = []
            for i in range(max(0, a), min(rows, a + 2)):
                for j in range(max(0, b), min(cols, b + 2)):
                   # if (i, j) != cell: 
                   # print(elevation_map[i][j]) 
                    new_list.append(elevation_map[i][j])         
            #print(new_list)
            sub_list.append(new_list) # Append sorted values into new list
    #print(sub_list)
    # Calculate average of each sorted list and
    # append them to the final list
    for lists in sub_list:
        count = 0
        num = 0
        
        for i in lists:
            num += i
            count += 1
        if comon == []:
            comon.append(num // count)
        elif comon != [] and len(comon) < (len(elevation_map) + 1)//2:
            comon.extend([num // count])
            
        if len(comon) == (len(elevation_map) + 1)//2:
           # print(len(comon))
            final_list.append(comon)
            comon = []
    
    #print(final_list)
    return final_list
