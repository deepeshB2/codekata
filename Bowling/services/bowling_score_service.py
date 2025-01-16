class BowlingScoreService:

    def calculate_bowling_score(self, rolls):
        score = 0
        roll_index = 0

        # A helper function to get the pins knocked down on a particular roll
        def get_roll(index):
            if rolls[index] == 'X':  # Strike
                return 10
            elif rolls[index] == '/':  # Spare
                return 10 - get_roll(index - 1)
            elif rolls[index] == '-':  # Miss
                return 0
            else:  # Numeric value
                return int(rolls[index])

        # Loop through the 10 frames
        for frame in range(10):
            if rolls[roll_index] == 'X':  # Strike case
                score += 10 + get_roll(roll_index + 1) + get_roll(roll_index + 2)
                roll_index += 1  # Move to the next roll
            elif rolls[roll_index + 1] == '/':  # Spare case
                score += 10 + get_roll(roll_index + 2)
                roll_index += 2  # Move to the next frame
            else:  # Open frame case
                score += get_roll(roll_index) + get_roll(roll_index + 1)
                roll_index += 2  # Move to the next frame

        return score
    # def calculate_score(self, rolls: str) -> int:
    #     """Calculate the total score for a bowling game."""
    #     frames = self.parse_frames(rolls)
    #     score = 0
    #     frame_index = 0
    #
    #     for frame in range(10):
    #         if frames[frame_index] == "X":  # Strike
    #             score += 10 + self.get_roll_value(frames, frame_index + 1) + self.get_roll_value(frames,
    #                                                                                              frame_index + 2)
    #             frame_index += 1
    #         elif "/" in frames[frame_index]:  # Spare
    #             score += 10 + self.get_roll_value(frames, frame_index + 1)
    #             frame_index += 1
    #         else:  # Open frame
    #             score += self.get_frame_value(frames[frame_index])
    #             frame_index += 1
    #
    #     return score
    #
    # def parse_frames(self, rolls: str):
    #     """Parse rolls into frames."""
    #     return rolls.split()
    #
    # def get_roll_value(self, frames, index):
    #     """Get the value of a single roll."""
    #     if index >= len(frames):
    #         return 0
    #     roll = frames[index]
    #     if roll == "X":
    #         return 10
    #     elif roll == "-":
    #         return 0
    #     elif roll.isdigit():
    #         return int(roll)
    #     else:
    #         raise ValueError("Invalid roll value")
    #
    # def get_frame_value(self, frame):
    #     """Get the total value of a frame."""
    #     if frame == "X":
    #         return 10
    #     elif "/" in frame:
    #         return 10
    #     else:
    #         return sum(self.get_roll_value(frame, i) for i in range(len(frame)))