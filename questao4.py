class BaseConhecimento:
    def __init__(self):
        self.regras = []  # Lista de regras (SE...ENTÃO...)
        self.fatos = set()  # Conjunto de fatos conhecidos
    
    def adicionar_regra(self, antecedente, consequente):
        self.regras.append((set(antecedente), consequente))
    
    def adicionar_fato(self, fato):
        self.fatos.add(fato)
    
    def obter_regras(self):
        return self.regras
    
    def obter_fatos(self):
        return self.fatos
    
    def limpar_fatos(self):
        self.fatos.clear()


class MotorInferencia:
    def __init__(self, base_conhecimento):
        self.base_conhecimento = base_conhecimento

    def encadeamento_para_frente(self):
        novos_fatos = True
        while novos_fatos:
            novos_fatos = False
            for antecedente, consequente in self.base_conhecimento.obter_regras():
                if antecedente.issubset(self.base_conhecimento.obter_fatos()) and consequente not in self.base_conhecimento.obter_fatos():
                    self.base_conhecimento.adicionar_fato(consequente)
                    novos_fatos = True

    def encadeamento_para_tras(self, objetivo, caminho=None):
        if caminho is None:
            caminho = []
        if objetivo in self.base_conhecimento.obter_fatos():
            return True, caminho + [objetivo]
        for antecedente, consequente in self.base_conhecimento.obter_regras():
            if consequente == objetivo:
                sub_caminho = []
                if all(self.encadeamento_para_tras(f, sub_caminho)[0] for f in antecedente):
                    self.base_conhecimento.adicionar_fato(consequente)
                    return True, sub_caminho + [objetivo]
        return False, caminho
    
    def encadeamento_misto(self, objetivo):
        self.encadeamento_para_frente()
        return self.encadeamento_para_tras(objetivo)


class Explicacao:
    def __init__(self, motor):
        self.motor = motor
    
    def porque(self, fato):
        sucesso, caminho = self.motor.encadeamento_para_tras(fato)
        if sucesso:
            return f"O fato '{fato}' é verdadeiro porque foi inferido a partir dos fatos: {caminho[:-1]} e levou a '{fato}'."
        return f"O fato '{fato}' não pôde ser provado."
    
    def como(self, fato):
        sucesso, caminho = self.motor.encadeamento_misto(fato)
        if sucesso:
            return f"O fato '{fato}' foi inferido através do seguinte caminho lógico: {caminho}."
        return f"Não há um caminho claro para inferir '{fato}'."


class Interface:
    def __init__(self, base_conhecimento, motor, explicacao):
        self.base_conhecimento = base_conhecimento
        self.motor = motor
        self.explicacao = explicacao

    def interagir(self):
        while True:
            entrada = input("Pergunte ou digite 'sair': ")
            if entrada.lower() == 'sair':
                break
            elif entrada.startswith("porque "):
                print(self.explicacao.porque(entrada[7:]))
            elif entrada.startswith("como "):
                print(self.explicacao.como(entrada[5:]))
            else:
                self.motor.encadeamento_para_frente()
                if entrada in self.base_conhecimento.obter_fatos():
                    print(f"Sim, {entrada} é verdadeiro.")
                else:
                    print(f"Não sei dizer se {entrada} é verdadeiro.")


# Exemplo
base = BaseConhecimento()
base.adicionar_regra(["A", "B"], "C")
base.adicionar_regra(["C"], "D")
base.adicionar_fato("A")
base.adicionar_fato("B")

motor = MotorInferencia(base)
explicacao = Explicacao(motor)
interface = Interface(base, motor, explicacao)

interface.interagir()
