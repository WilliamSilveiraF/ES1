from enum import Enum

class BoardHouse(Enum):
    INIT = (0, 'Init House', 'Today is your lucky day! By passing at the beginning, you have won U$$ 10000.', 10000)
    GRADUATION = (1, 'You graduated', 'Congratulations, you graduated!! With that you must pay tuition of U$$ 20000 from your college.', -20000)
    BIRTH = (2, 'Birth', 'Congratulations, a new child has joined your family!. Remember, with every joy comes new responsibilities. Each turn you must pay U$$ 500 by child.', 0)
    LOTTERY = (3, 'Lottery', "You've won the lottery! Collect an immediate U$$ 75000 bonus to represent your winnings.", 75000)
    MOUNT_EVEREST = (4, 'Mount Everest Expedition', "You've decided to climb Mount Everest! Pay U$$ 5000 to cover the expedition costs.", -5000)
    PROMOTION = (5, 'Promotion', 'Congratulations, your salary increases by 10 percent.', 0)
    ADOPTION = (6, 'Adoption', 'Your heart and home have expanded with the adoption of a child. Celebrate this moment and remember, every child is a bundle of joy and a responsibility to shape the future. Each turn you must pay U$$ 500 by child.', 0)
    ROBBERY = (7, 'Robbery', "Unfortunately, you've been robbed. Pay U$$ 10000 to represent the financial loss.", -10000)
    BACKPACKING = (8, 'Backpacking Trip', "You've decided to go backpacking through Europe! Pay U$$ 15000 to cover the trip costs.", -15000)
    INTERNSHIP = (9, 'Internship', 'You have landed an internship in your field! This is a great step towards your career. You will gain valuable experience, but you will earn only half your salary this turn as internships are typically low-paying.', 0)
    CHILD_GRADUATION = (10, "Child's Graduation", 'Your child has hit a significant milestone - university graduation! This proud moment comes with expenses. Make a U$$ 5000 payment to cover the cost of the graduation ceremony, from the gown to the celebratory dinner.', -5000)
    INVESTMENT = (11, 'Investment', "You've decided to invest some money. You will gain U$$ 12500.", 12500)
    CORAL_REEF_DIVE = (12, 'Coral Reef Dive', "You've decided to dive in the Coral Reef! Pay U$$ 6000 to cover the dive costs.", -6000)
    POST_GRADUATION = (13, 'Post-Graduation', 'You have completed your postgraduate studies! This milestone is an important step in your career and deserves a reward. Collect U$$ 10000 bonus to reflect your increased qualifications.', 10000)
    SCHOOL_CHANGE = (14, 'School Change', "Your child's education journey requires a school change. Whether it's due to a move or just seeking better opportunities, there are costs involved. Pay U$$ 7000 for the move, new uniforms, and other related expenses.", -7000)
    LIFE_INSURANCE = (15, 'Life Insurance', "You've decided to buy life insurance. Pay U$$ 10000 to represent the insurance premium.", 0) 
    MARATHON = (16, 'Marathon', "You've decided to run a marathon! Pay U$$ 2500 to cover the registration and training costs.", -2500)
    ENTREPRENEUR = (17, 'Entrepreneur', 'You have taken the bold step of starting your own business! This exciting venture comes with its costs. Pay U$$ 25000 to cover the startup costs.', -25000)
    BIRTHDAY_PARTY = (18, 'Birthday Party', "It's time to celebrate! One of your children has a birthday. You're throwing a party complete with cake, games, and party favors. Pay U$$ 7500 for the party expenses.", -7500)
    INHERITANCE = (19, 'Inheritance', "You've inherited a large sum of money. Collect U$$ 100000 bonus to represent the inheritance.", 100000)
    SPACE_TRAVEL = (20, 'Space Travel', "You've decided to go to space! Pay U$$ 30000 to cover the travel costs.", -30000)
    RETIREMENT = (21, 'Retirement', "You've retired after a long and successful career! It's time to relax and enjoy the fruits of your labor. Now, you will collect U$$ 5000 bonus each turn.", 0)
    CHILDREN_WEDDING = (22, "Children's Wedding", "Your child is getting married! A proud and emotional moment for you. However, weddings can be expensive. Pay U$$ 17500 for the wedding party, from the venue to the food and the decorations.", -17500)
    CAR_INSURANCE = (23, 'Car Insurance', "You've decided to buy car insurance. Pay U$$ 8000 amount to represent the insurance premium.", 0)
    AFRICAN_SAFARI = (24, 'African Safari', "You've decided to go on a safari in Africa! Pay U$$ 16000 amount to cover the trip costs.", -16000)
    CAREER_CHANGE = (25, 'Career Change', 'You have decided to change your career! This brave move opens up new opportunities, your salary increases by 20 percent.', 0)
    MUSIC_LESSON = (26, 'Music Lesson', 'Your children have shown an interest in music and want to learn an instrument. This could be the start of a lifelong passion or even a career. Pay U$$ 2500 for the music lessons, including the cost of the instrument and the tutor.', -2500)
    INCOME_TAX = (27, 'Income Tax', "It's income tax time. Pay 30 percent of your total money to represent your taxes.", 0)
    ANTARCTIC_EXPEDITION = (28, 'Antarctic Expedition', "You've decided to visit Antarctica! Pay U$$ 22500 to cover the trip costs.", -22500)
    VOLUNTEER_WORK = (29, 'Volunteer Work', 'You have decided to do volunteer work. This noble act might not provide a salary this turn, but it brings a great sense of fulfillment.', 0)
    SPORTS_COMPETITION = (30, 'Sports Competition', "Your children have entered a sports competition! They're excited and nervous. Pay U$$ 3000 for the sports equipment, team uniforms, and other related expenses.", -3000)
    CHARITY_HOUSE = (31, 'Charity House', "You've decided to make a generous donation to a charity that's close to your heart. Pay U$$ 10000 amount to represent your charitable contribution.", -10000)
    MOTORCYCLE_JOURNEY = (32, 'Motorcycle Journey on Route 66', "You've decided to ride Route 66 on a motorcycle! Pay U$$ 8000 to cover the trip costs.", -8000)
    REMOTE_WORK = (33, 'Remote Work', 'You have landed the opportunity to work remotely! This gives you more flexibility and time to spend with family or on hobbies. Receive your normal salary this turn and gain U$$ 3000 bonus to represent the savings on transportation and work clothes.', 3000)
    FAMILY_TRIP = (34, 'Family Trip', "Quality time alert! You're taking a well-deserved family trip. It's time for relaxation and adventures. Pay U$$ 12000 for the trip expenses, including travel, accommodation, and daily allowances.", -12000)
    WINDFALL = (35, 'Windfall', "You've received an unexpected windfall, perhaps from a forgotten investment or a distant relative. Collect U$$ 20000 bonus to represent the unexpected influx of money.", 20000)

    def __init__(self, posicao, title, description, transaction):
        self.posicao = posicao
        self.title = title
        self.description = description
        self.transaction = transaction

    def handle_event(self, jogador):
        casa_handlers = {
            BoardHouse.BIRTH: jogador.add_child,
            BoardHouse.ADOPTION: jogador.add_child,
            BoardHouse.PROMOTION: jogador.increase_salary_10_percent,
            BoardHouse.INTERNSHIP: jogador.handle_internship,
            BoardHouse.LIFE_INSURANCE: jogador.buy_life_insurance,
            BoardHouse.CAR_INSURANCE: jogador.buy_car_insurance,
            BoardHouse.RETIREMENT: jogador.set_retirement,
            BoardHouse.CAREER_CHANGE: jogador.increase_salary_20_percent,
            BoardHouse.INCOME_TAX: jogador.apply_income_tax,
            BoardHouse.VOLUNTEER_WORK: jogador.handle_volunter_work,
        }
        handler = casa_handlers.get(self)
        if handler:
            handler()

    @classmethod
    def from_posicao(cls, posicao):
        for casa in cls:
            if casa.posicao == posicao:
                return casa
        raise ValueError(f"{posicao} is not a valid Casa posicao")
