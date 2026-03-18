
def mergeListByKey(list1, list2, key):
  merged_dict = {}

  for item in list1:
      item_id = item.get(key)
      if item_id is not None:
          merged_dict[item_id] = item.copy()

  for item in list2:
      item_id = item.get(key)
      if item_id is not None:
          if item_id in merged_dict:
              merged_dict[item_id].update(item)
          else:
              merged_dict[item_id] = item.copy()

  return list(merged_dict.values())