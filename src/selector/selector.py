class Selector:
    def select_device(self, openqasm_circuit: str, openqasm_version: int) -> str:
        raise NotImplementedError
