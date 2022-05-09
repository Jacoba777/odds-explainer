class Event:
    desc: str
    pos: str
    neg: str
    prob: float
    can_repeat: bool
    can_invert: bool
    ratio: float

    def __init__(self, prob=0.0, desc="", pos="", neg="", can_repeat=False, can_invert=True, ratio=1.0):
        self.desc = desc
        self.prob = prob
        self.can_repeat = can_repeat
        self.can_invert = can_invert
        self.pos = pos
        self.neg = neg
        self.ratio = ratio


def eval_events(events: list):
    best_event: Event = Event()

    for event in events:
        local_best_ratio = 1
        freq = 1

        while freq <= 5:
            prob = pow(event.prob, freq)
            ratio = prob / target
            if ratio < 1:
                ratio = 1 / ratio

            if ratio < best_event.ratio:
                best_event = Event(prob, event.desc.replace("@", event.pos) + " " + freq_disp(freq), event.pos, event.neg, False, False, ratio)

            if ratio >= local_best_ratio or not event.can_repeat:
                break
            freq = freq + 1
            local_best_ratio = ratio

        local_best_ratio = 1
        freq = 1
        while freq <= 5 and event.can_invert:
            prob = 1 - pow(event.prob, freq)
            ratio = abs(prob - target)

            if ratio < best_event.ratio:
                best_event = Event(prob, event.desc.replace("@", event.neg) + " " + freq_disp(freq), event.pos, event.neg,
                                   False, False, ratio)

            if ratio >= local_best_ratio or not event.can_repeat:
                break
            freq = freq + 1
            local_best_ratio = ratio

        if best_event.ratio == 0:
            break

    return best_event


def exact_or_approx(ratio):
    if ratio == 0:
        return "exactly"
    else:
        return "approximately"


def freq_disp(freq):
    if freq > 1:
        return str(freq) + " times in a row"
    else:
        return ""


def approx_print(ratio, prob):
    if ratio > 0:
        return "(" + str(prob) + ")"
    else:
        return ""


print("Enter your probability as a decimal (1% being 0.01):")
target = float(input())

events = (
    Event(1.0, "the sun @ rise tomorrow", "will", "will not"),
    Event(1/2, "of getting @ on a coin flip", "heads", "tails", True, False),
    Event(1/2, "of getting @ at least once when flipping a coin", "heads", "tails", True, True),
    Event(2/6, "of getting a @ on a dice roll", "5 or 6", "4 or lower"),
    Event(1/6, "of getting a @ on a dice roll", "6", "5 or lower", True, False),
    Event(1/7, "a randomly selected person was born on @", "a Monday", "any day other than Monday"),
    Event(1/13, "a random card drawn from a full deck @ an Ace", "being", "being anything other than"),
    Event(1/52, "a random card drawn from a full deck @ an Ace of Spades", "being", "being anything other than"),
    Event(9/10, "a randomly selected person is @", "right-handed", "left-handed"),
    Event(8/100, "a randomly selected person @ blue eyes", "has", "does not have"),
    Event(75/100, "a randomly selected person @ brown eyes", "has", "does not have"),
    Event(1/12.5, "a randomly selected American @ in Texas", "lives", "does not live"),
    Event(18/10000, "a randomly selected American @ in Wyoming", "lives", "does not live"),
    Event(1/3000, "@ stuck by lightning in your lifetime", "being", "not being"),
    Event(33/1000, "a pregnancy leading to @", "twins", "anything but twins"),
    Event(2/100, "a randomly selected Harvard application is @", "accepted", "rejected"),
    Event(1/300000000, "of @ the Powerball", "winning", "losing", True),
    Event(8/100, "of @ the age of 100", "living to", "dying before"),
    Event(23/209, "a randomly selected American is @", "illiterate", "literate"),
    Event(4.5/100, "a randomly selected American is @", "LGBT", "straight and cisgender"),
    Event(88/100, "a randomly selected American @", "graduated high school", "dropped out of high school"),
    Event(1/8192, "@encountering a shiny Pokemon", "", "not ", True),
        )

event = eval_events(events)

print("The odds of this event happening is", str(target) + ", or", exact_or_approx(event.ratio), "the odds", event.desc, approx_print(event.ratio, event.prob))
