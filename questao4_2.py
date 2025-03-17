class BaseConhecimento:
    def __init__(self):
        self.regras = []  # Lista de regras (SE...ENTÃO...)
        self.fatos = set()  # Conjunto de fatos conhecidos
    
    def adicionar_regra(self, antecedente, consequente):
        """Adiciona uma regra à base de conhecimento."""
        self.regras.append((set(antecedente), consequente))
    
    def adicionar_fato(self, fato):
        """Adiciona um fato à base de conhecimento."""
        self.fatos.add(fato)
    
    def obter_regras(self):
        """Retorna todas as regras."""
        return self.regras
    
    def obter_fatos(self):
        """Retorna todos os fatos."""
        return self.fatos
    
    def limpar_fatos(self):
        """Limpa todos os fatos da base de conhecimento."""
        self.fatos.clear()


class MotorInferencia:
    def __init__(self, base_conhecimento):
        self.base_conhecimento = base_conhecimento

    def encadeamento_para_frente(self):
        """Encadeamento para frente: infere novos fatos a partir das regras e fatos existentes."""
        novos_fatos = True
        while novos_fatos:
            novos_fatos = False
            for antecedente, consequente in self.base_conhecimento.obter_regras():
                if antecedente.issubset(self.base_conhecimento.obter_fatos()) and consequente not in self.base_conhecimento.obter_fatos():
                    self.base_conhecimento.adicionar_fato(consequente)
                    novos_fatos = True

    def encadeamento_para_tras(self, objetivo, caminho=None):
        """Encadeamento para trás: tenta inferir um objetivo a partir das regras e fatos existentes."""
        if caminho is None:
            caminho = []
        
        # Evita loops infinitos verificando se o objetivo já está no caminho
        if objetivo in caminho:
            return False, caminho
        
        # Se o objetivo já está na base de conhecimento, retorna o caminho atual
        if objetivo in self.base_conhecimento.obter_fatos():
            return True, caminho + [objetivo]
        
        # Tenta inferir o objetivo a partir das regras
        for antecedente, consequente in self.base_conhecimento.obter_regras():
            if consequente == objetivo:
                sub_caminho = []
                # Verifica se todos os antecedentes da regra podem ser inferidos
                if all(self.encadeamento_para_tras(f, sub_caminho)[0] for f in antecedente):
                    return True, sub_caminho + [objetivo]
        
        # Se o objetivo não puder ser inferido, retorna False
        return False, caminho
    
    def encadeamento_misto(self, objetivo):
        """Encadeamento misto: combina encadeamento para frente e para trás."""
        self.encadeamento_para_frente()
        return self.encadeamento_para_tras(objetivo)


class Explicacao:
    def __init__(self, motor):
        self.motor = motor
    
    def porque(self, fato):
        """Explica por que um fato é verdadeiro."""
        sucesso, caminho = self.motor.encadeamento_para_tras(fato)
        if sucesso:
            return f"O fato '{fato}' é verdadeiro porque foi inferido a partir dos fatos: {caminho[:-1]}."
        return f"O fato '{fato}' não pôde ser provado."
    
    def como(self, fato):
        """Explica como um fato foi inferido."""
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
        """Interface de diálogo com o usuário."""
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


# Exemplo de uso
if __name__ == "__main__":
    # Cria a base de conhecimento
    base = BaseConhecimento()
    base.adicionar_regra(["A", "B"], "C")
    base.adicionar_regra(["C"], "D")
    base.adicionar_fato("A")
    base.adicionar_fato("B")

    # Cria o motor de inferência e o módulo de explicação
    motor = MotorInferencia(base)
    explicacao = Explicacao(motor)

    # Cria a interface e inicia a interação
    interface = Interface(base, motor, explicacao)
    interface.interagir()
