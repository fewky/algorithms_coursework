
from parser import ExpressionTree
from visualizer import Visualizer

def main():
    print("ДЕРЕВО ВЫРАЖЕНИЙ\n")
    print("Поддерживаемые операции: + - * / ^")

    tree_builder = ExpressionTree()
    
    while True:
        print("\nВведите выражение (или 'exit' для выхода):")
        expression = input("> ")
        
        if expression.lower() == 'exit':
            print("Выход из программы.")
            break
        
        if not expression:
            print("Ошибка: Пустой ввод")
            continue
        
        is_valid, error_msg = tree_builder.validate_expression(expression)
        if not is_valid:
            print(f"Некорректный ввод: {error_msg}. Попробуйте снова.")
            continue
        
        try:
            tokens = tree_builder.tokenize(expression)
            print(f"\nТокены: {tokens}")
            
            root = tree_builder.build_tree(tokens)
            
            if root is None:
                print("Ошибка: Не удалось построить дерево")
                continue
            
            result = tree_builder.evaluate(root)
            print(f"\nРезультат вычисления: {result}")
            
            print("\nРазные формы записи выражения:")
            print(f"Инфиксная:  {tree_builder.to_infix(root)}")
            print(f"Префиксная: {tree_builder.to_prefix(root)}")
            print(f"Постфиксная: {tree_builder.to_postfix(root)}\n")
            
            print("ВИЗУАЛИЗАЦИЯ ДЕРЕВА:\n")
            Visualizer.visualize(root)
            
        except ZeroDivisionError as e:
            print(f"Ошибка вычисления: {e}")
        except ValueError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")

if __name__ == "__main__":
    main()