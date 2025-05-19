class Colors:
    dark_grey   = (36, 41, 51)     # fundo mais neutro e elegante
    green       = (88, 199, 89)    # verde suave
    red         = (220, 80, 80)    # vermelho suave
    orange      = (245, 160, 90)   # laranja pastel
    yellow      = (240, 220, 90)   # amarelo suave
    purple      = (180, 120, 255)  # roxo lavanda
    cyan        = (100, 220, 230)  # ciano suave
    blue        = (100, 140, 255)  # azul claro
    white       = (230, 230, 230)  # branco apagado (bom para dark mode)
    dark_blue   = (50, 60, 100)    # azul escuro refinado
    light_blue  = (90, 130, 200)   # azul claro suave

    @classmethod
    def get_cell_colors(cls):
        return [cls.dark_grey, cls.green, cls.red, cls.orange, cls.yellow, cls.purple, cls.cyan, cls.blue]
