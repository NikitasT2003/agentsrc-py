from agentsrc.analysis.ast_symbols import ASTAnalyzer

def test_ast_analyzer(tmp_path):
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    
    mock_file = src_dir / "models.py"
    mock_file.write_text('''
"""Module docstring"""
import os

class User(Base):
    """User docstring"""
    def get_name(self):
        pass

def fetch_data(url: str):
    pass

class FetchError(Exception):
    pass
''')

    analyzer = ASTAnalyzer()
    symbol_map = analyzer.analyze_directory(str(src_dir))
    
    assert len(symbol_map.modules) == 1
    assert symbol_map.modules[0].name == "models"
    assert symbol_map.modules[0].docstring == "Module docstring"
    
    class_names = [c.name for c in symbol_map.classes]
    assert "User" in class_names
    user_class = next(c for c in symbol_map.classes if c.name == "User")
    assert user_class.docstring == "User docstring"
    assert "Base" in user_class.bases
    assert "get_name" in user_class.methods
    
    func_names = [f.name for f in symbol_map.functions]
    assert "fetch_data" in func_names
    
    exc_names = [e.name for e in symbol_map.exceptions]
    assert "FetchError" in exc_names
