import numpy as np

class EditData ():
    def check_length(self, item1, item2):
        if (len(item1) + len(item2)) == 1:
            if len(item1) == 1:
                data = item1
            else:
                data = item2
        else:
            data = np.append(item1 , item2)
        return data

    def fix_data(self, item):
        """
        does everything in one function, might be a bit slow.
        :param item:
        :return:
        """
        if len(item['REPLIES_TODAY']) > 0:
            new_list = []
            for reply in item['REPLIES_TODAY']:
                new_list.append(int(reply[1:-1]))
            item['REPLIES_TODAY'] = new_list
        if len(item['REPLIES_YESTERDAY']) > 0:
            new_list = []
            for reply in item['REPLIES_YESTERDAY']:
                new_list.append(int(reply[1:-1]))
            item['REPLIES_YESTERDAY'] = new_list

        if len(item['VIEWS_TODAY']) > 0:
            new_list = []
            for reply in item['VIEWS_TODAY']:
                new_list.append(int(reply.strip()))
            item['VIEWS_TODAY'] = new_list
        if len(item['VIEWS_YESTERDAY']) > 0:
            new_list = []
            for reply in item['VIEWS_YESTERDAY']:
                new_list.append(int(reply.strip()))
            item['VIEWS_YESTERDAY'] = new_list

        thread = np.append(item['THREAD_KEY_TODAY'],item['THREAD_KEY_YESTERDAY'])
        views = self.check_length(item['VIEWS_TODAY'],item['VIEWS_YESTERDAY'] )
        replies = self.check_length(item['REPLIES_TODAY'],item['REPLIES_YESTERDAY'])
        items = {}
        for i in range(len(thread)):
            items[thread[i]] = [views [i], replies[i]]
        return items
