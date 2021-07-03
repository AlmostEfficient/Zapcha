test = {'0': False, '1': True, '2': False, '3': False, '4': True, '5': False, '6': False, '7': False, '8': False}

targets = []
for item in test:
    # print(item)
    if test[item] is True:
        targets.append(item)

ts = (', ').join(targets)
# for target in targets:
    # ts = ts + " " + target

print(ts)