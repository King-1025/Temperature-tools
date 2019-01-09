# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 08:04:59 2018

@author: chaos
"""

import os
import struct

# Convert to human readable format
def format_size_human_readable(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%fG" % (G)
        else:
            return "%fM" % (M)
    else:
        return "%fkb" % (kb)
    
# get file size
def get_file_size_single(path, b_human_readable):
    try:
        size = os.path.getsize(path)
        if (b_human_readable):
            return format_size_human_readable(size)
        # Else
        return size
    except Exception as err:
        print(err)


# get file size all
def getFileSize(path, b_human_readable):
    sumsize = 0
    try:
        filename = os.walk(path)
        for root, dirs, files in filename:
            for fle in files:
                size = os.path.getsize(path + fle)
                sumsize += size
        if (b_human_readable):
            return format_size_human_readable(sumsize)
        # Else
        return sumsize
    except Exception as err:
        print(err)


"""
Write an array of double into memory.
"""
def BinaryRectifyCoefficientReader(filename):
    lst_content = []
    need_load_previous_version = True
    if False == os.path.exists(filename):
        need_load_previous_version = False
        return need_load_previous_version, lst_content 
    
    # Check the size of the open file.       
    size_f = get_file_size_single(filename, False)
    if size_f <= 0:
        need_load_previous_version = False
        return need_load_previous_version, lst_content 
    
    # Else read
    with open(filename, "rb") as file:
        # Reade the head
        (version) = struct.unpack("2s",file.read(2))
        (n_entry) = struct.unpack("i",file.read(4))
        lst_content.extend([version])
        lst_content.extend([n_entry[0]])
        
        item = []
        # Read each line
        for entry in range(n_entry[0]):
            distance, alpha, beta, gamma = struct.unpack("dddd",file.read(8 + 8 + 8 + 8))
            item.append([distance, alpha, beta, gamma])
        
        lst_content.append(item)
        need_load_previous_version = True;
    # Return
    return need_load_previous_version, lst_content
    
def BinaryRectifyCoefficientWriter(filename, distance, alpha, beta, gamma, version = 'v1'):
    # Read previous version.
    # Structure of the content
    # version, item count, [d, a, b, c]
    need_create_head_counter, prev_content = BinaryRectifyCoefficientReader(filename)
    # Check the version?
    n_item_to_write = 0 if False == need_create_head_counter else prev_content[1]
    n_item_to_write = n_item_to_write + 1
    
    with open(filename, "wb+") as file:
        file.write(struct.pack("2s", version.encode("utf-8")))
        file.write(struct.pack("i", n_item_to_write))
        for item in range(n_item_to_write - 1):
            # Output the previous content
            distance_ = prev_content[2][item][0]
            alpha_    = prev_content[2][item][1]
            beta_     = prev_content[2][item][2]
            gamma_    = prev_content[2][item][3]
            
            file.write(struct.pack("dddd", distance_, alpha_, beta_, gamma_))
        # The new record.
        file.write(struct.pack("dddd", distance, alpha, beta, gamma))
        
    return

if __name__ == '__main__':
    filename = "null.data"
    distance = 4.0
    alpha    = 1.0
    beta     = 1.0
    gamma    = 0.0
    
    BinaryRectifyCoefficientWriter(filename, distance, alpha, beta, gamma)
    
 #   distance = 5.0
 #   alpha    = 34.567788
 #   beta     = 1000.982376
 #   gamma    = -0.98762
    
 #   BinaryRectifyCoefficientWriter(filename, distance, alpha, beta, gamma)
    
    