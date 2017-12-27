# coding: utf-8


class Blocks:
    def blocks_normalize(self, blocks):
        left = 1e10
        right = -1e10
        top = 1e10
        bottom = -1e10
        for block in blocks:
            if left > block['x']:
                left = block['x']
            if right < block['x'] + block['w']:
                right = block['x'] + block['w']
            if top > block['y']:
                top = block['y']
            if bottom < block['y'] + block['h']:
                bottom = block['y'] + block['h']

        for block in blocks:
            block['x'] -= left
            block['y'] -= top

            block['x'] = float(block['x']) / (float(right) - float(left))
            block['y'] = float(block['y']) / (float(bottom) - float(top))
            block['w'] = float(block['w'] / (float(right) - float(left)))
            block['h'] = float(block['h']) / (float(bottom) - float(top))
        return blocks

    def find_common(self, x, y):
        result = None
        distance = 1e10
        for block in self.blocks:
            distance_x = abs(x - block['x'])
            distance_y = abs(y - block['y'])
            if (distance_x + distance_y > distance):
                continue

            distance = distance_x + distance_y
            result = block['text']

        if not result:
            self.errors.append("603: Region not found")
            return

        return result
