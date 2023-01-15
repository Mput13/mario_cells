import pygame


# Check if B collide on left of A
#
# @param  object A The First sprite to check collision to
# @param  object B The second sprite wich would collide A on left
# @return bool     The result of the test
def left(A, B):
    # First check if A & B collide themselves
    if pygame.sprite.collide_rect(A, B):

        # Check if right points of B are in A but not left points of B
        if A.rect.collidepoint(B.rect.midright) and (
                A.rect.collidepoint(B.rect.topright) or
                A.rect.collidepoint(B.rect.bottomright)) and \
                not A.rect.collidepoint(B.rect.midleft) and (
                not A.rect.collidepoint(B.rect.topleft) or
                not A.rect.collidepoint(B.rect.bottomleft)):
            return True

    # Instead return False
    return False


#
# Check if B collide on right of A
#
# @param  object A The First sprite to check collision to
# @param  object B The second sprite wich would collide A on right
# @return bool     The result of the test
def right(A, B):
    # First check if A & B collide themselves
    if pygame.sprite.collide_rect(A, B):

        # Check if left points of B are in A but not right points of B
        if A.rect.collidepoint(B.rect.midleft) and (
                A.rect.collidepoint(B.rect.topleft) or
                A.rect.collidepoint(B.rect.bottomleft)) and \
                not A.rect.collidepoint(B.rect.midright) and (
                not A.rect.collidepoint(B.rect.topright) or
                not A.rect.collidepoint(B.rect.bottomright)):
            return True

    # Instead return False
    return False


#
# Check if B collide on top of A
#
# @param  object A The First sprite to check collision to
# @param  object B The second sprite wich would collide A on top
# @return bool     The result of the test
def top(A, B):
    # First check if A & B collide themselves
    if pygame.sprite.collide_rect(A, B):

        # Check if bottom points of B are in A but not top points of B
        if A.rect.collidepoint(B.rect.midbottom) and (
                A.rect.collidepoint(B.rect.bottomleft) or
                A.rect.collidepoint(B.rect.bottomright)) and \
                not A.rect.collidepoint(B.rect.midtop) and (
                not A.rect.collidepoint(B.rect.topleft) or
                not A.rect.collidepoint(B.rect.topright)):
            return True

    # Instead return False
    return False


#
# Check if B collide on bottom of A
#
# @param  object A The First sprite to check collision to
# @param  object B The second sprite wich would collide A on bottom
# @return bool     The result of the test
def bottom(A, B):
    # First check if A & B collide themselves
    if pygame.sprite.collide_rect(A, B):

        # Check if top points of B are in A but not bottom points of B
        if A.rect.collidepoint(B.rect.midtop) and (
                A.rect.collidepoint(B.rect.topleft) or
                A.rect.collidepoint(B.rect.topright)) and \
                not A.rect.collidepoint(B.rect.midbottom) and (
                not A.rect.collidepoint(B.rect.bottomleft) or
                not A.rect.collidepoint(B.rect.bottomright)):
            return True

    # Instead return False
    return False


#
# Sets multiple side detection
#
class _Multiple:

    #
    # Inits __Multiple class
    #
    # @param  object self  The class itself
    # @param  list   sides The sides wich has to be detected
    # @return void
    def __init__(self, sides):
        self.sides = sides

    #
    # Checks detection on multiple sides
    #
    # @param  object self The class itself
    # @param  object A    The first sprite
    # @param  object B    The second sprite
    # @return bool        The result of the tests
    def check_sides(self, A, B):

        # Array keeping already done sides test for not repeating tasks
        done_sides = []
        collisions = {}

        # Navigate trough list
        for side in self.sides:

            # Check if side test was done before
            if side not in done_sides:

                # Insert that element
                done_sides.append(side)

                # Check for left if selected
                if side == "left":
                    collisions["left"] = left(A, B)

                # Check for right if selected
                elif side == "right":
                    collisions["right"] = right(A, B)

                # Check for top if selected
                elif side == "top":
                    collisions["top"] = top(A, B)
                # Check for bottom if selected
                elif side == "bottom":
                    collisions["bottom"] = bottom(A, B)
                # Error if invalid side name
                else:
                    print("Unknown side name passed in multiple side detections: \"" + str(side) + "\"")
        return collisions

    #
    # Checks detection on multiple sides (with group support)
    #
    # @param  object self The class itself
    # @param  object A    The first sprite
    # @param  object B    The second sprite
    # @return bool        The result of the tests
    def check_sides_group(self, A, B):
        return self.check_sides(B, A)
