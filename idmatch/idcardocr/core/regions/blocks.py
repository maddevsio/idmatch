# coding: utf-8


class Blocks:
    def blocks_normalize(self, blocks):
        for block in blocks:
            block['x'] = float(block['x']) / float(self.size[0])
            block['y'] = float(block['y']) / float(self.size[1])
            block['w'] = float(block['w']) / float(self.size[0])
            block['h'] = float(block['h']) / float(self.size[1])
            print(block['x'], block['y'])
            print(block['text'])
        return blocks

    def find_common(self, x, y):
        result = None
        for block in self.blocks:
            if block['x']*0.95 <= x <= (block['x']+block['w'])*1.1:
                if block['y']*0.95 <= y <= (block['y']+block['h'])*1.1:
                    return block['text']

        if not result:
            self.errors.append("603: Region not found")
            return

        return result
