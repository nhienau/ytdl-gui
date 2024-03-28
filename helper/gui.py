def set_textbox_value(textbox, message):
    textbox.configure(state="normal")
    textbox.delete("0.0", "end")
    textbox.insert("0.0", text=message)
    textbox.configure(state="disabled")

def move_rows_up(lst, selected):
    sorted_selected_index = sorted(selected)
    if sorted_selected_index[0] == 0:
        lst = lst[1:] + [lst[0]]
    else:
        for index in sorted_selected_index:
            lst[index], lst[index - 1] = lst[index - 1], lst[index]
    selected = list(map(lambda row: row - 1 if row != 0 else len(lst) - 1, selected))
    return lst, selected

def move_rows_down(lst, selected):
    sorted_selected_index = sorted(selected, reverse=True)
    if sorted_selected_index[0] == len(lst) - 1:
        lst = [lst[-1]] + lst[:-1]
    else:
        for index in sorted_selected_index:
            lst[index], lst[index + 1] = lst[index + 1], lst[index]
    selected = list(map(lambda row: row + 1 if row != len(lst) - 1 else 0, selected))
    return lst, selected

def move_rows_to_top(lst, selected):
    sorted_selected_index = sorted(selected)
    new_list = [lst[i] for i in sorted_selected_index] + [el for i, el in enumerate(lst) if i not in sorted_selected_index]
    new_selected_index = [new_list.index(lst[i]) for i in selected]
    return new_list, new_selected_index

def move_rows_to_bottom(lst, selected):
    sorted_selected_index = sorted(selected)
    new_list = [el for i, el in enumerate(lst) if i not in sorted_selected_index] + [lst[i] for i in sorted_selected_index]
    new_selected_index = [new_list.index(lst[i]) for i in selected]
    return new_list, new_selected_index
