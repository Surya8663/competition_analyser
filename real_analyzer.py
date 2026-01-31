# real_analyzer.py - COMPLETE FIXED CODE
import os
import json
import re
import ast
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set

class RealRepositoryAnalyzer:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
    
    def analyze_deep(self) -> Dict:
        """DEEP analysis - reads files, understands code, extracts REAL data"""
        try:
            return {
                'metadata': self._analyze_metadata(),
                'structure': self._analyze_structure(),
                'files': self._analyze_files(),
                'code_quality': self._analyze_code_quality(),
                'dependencies': self._analyze_dependencies(),
                'documentation': self._analyze_documentation(),
                'testing': self._analyze_testing(),
                'docker': self._analyze_docker(),
                'ci_cd': self._analyze_ci_cd(),
                'challenge_specific': self._analyze_challenge_specific(),
                'key_files_content': self._extract_key_files(),
                'stats': self._calculate_stats(),
                'code_patterns_found': self._analyze_code_patterns()
            }
        except Exception as e:
            return {'error': f"Deep analysis error: {str(e)}"}
    
    def _analyze_metadata(self) -> Dict:
        """Extract repository metadata"""
        metadata = {
            'has_readme': False,
            'has_license': False,
            'has_gitignore': False,
            'has_test_directory': False,
            'has_dockerfile': False,
            'total_files': 0,
            'total_lines': 0,
            'repo_size_mb': 0
        }
        
        # Count files and lines
        total_files = 0
        total_lines = 0
        
        for root, dirs, files in os.walk(self.repo_path):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if file.startswith('.'):
                    continue
                
                file_path = Path(root) / file
                total_files += 1
                
                # Count lines for code files
                if file_path.suffix in ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c']:
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            total_lines += len(f.readlines())
                    except:
                        continue
        
        metadata['total_files'] = total_files
        metadata['total_lines'] = total_lines
        
        # Check for key files
        for item in self.repo_path.iterdir():
            if item.is_file():
                name_lower = item.name.lower()
                if name_lower.startswith('readme'):
                    metadata['has_readme'] = True
                elif 'license' in name_lower:
                    metadata['has_license'] = True
                elif name_lower == '.gitignore':
                    metadata['has_gitignore'] = True
                elif 'dockerfile' in name_lower:
                    metadata['has_dockerfile'] = True
        
        # Check for test directory
        test_dirs = ['tests', 'test', '__tests__']
        for test_dir in test_dirs:
            if (self.repo_path / test_dir).exists():
                metadata['has_test_directory'] = True
                break
        
        # Calculate repo size
        total_size = 0
        for root, dirs, files in os.walk(self.repo_path):
            for file in files:
                file_path = Path(root) / file
                try:
                    total_size += file_path.stat().st_size
                except:
                    continue
        
        metadata['repo_size_mb'] = round(total_size / (1024 * 1024), 2)
        
        return metadata
    
    def _analyze_structure(self) -> Dict:
        """Analyze directory structure"""
        structure = {
            'key_directories': {},
            'architecture_patterns': []
        }
        
        key_dirs = ['src', 'app', 'lib', 'core', 'api', 'routes', 'models', 
                   'tests', 'test', 'docs', 'documentation', 'docker', 
                   'deploy', 'config', 'configuration', 'data', 'etl']
        
        for dir_name in key_dirs:
            if (self.repo_path / dir_name).exists():
                structure['key_directories'][dir_name] = True
        
        # Detect architecture patterns
        if 'src' in structure['key_directories']:
            structure['architecture_patterns'].append('src-based')
        if 'app' in structure['key_directories']:
            structure['architecture_patterns'].append('app-based')
        if 'tests' in structure['key_directories'] or 'test' in structure['key_directories']:
            structure['architecture_patterns'].append('test-separated')
        if 'config' in structure['key_directories'] or 'configuration' in structure['key_directories']:
            structure['architecture_patterns'].append('config-separated')
        
        return structure
    
    def _analyze_files(self) -> Dict:
        """Analyze file types and counts"""
        files = {
            'python_count': 0,
            'javascript_count': 0,
            'typescript_count': 0,
            'html_count': 0,
            'css_count': 0,
            'json_count': 0,
            'yaml_count': 0,
            'markdown_count': 0,
            'largest_files': [],
            'code_file_details': []
        }
        
        # Count files by type
        for root, dirs, filenames in os.walk(self.repo_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for filename in filenames:
                if filename.startswith('.'):
                    continue
                
                file_path = Path(root) / filename
                ext = file_path.suffix.lower()
                
                if ext == '.py':
                    files['python_count'] += 1
                elif ext in ['.js', '.jsx']:
                    files['javascript_count'] += 1
                elif ext in ['.ts', '.tsx']:
                    files['typescript_count'] += 1
                elif ext == '.html':
                    files['html_count'] += 1
                elif ext in ['.css', '.scss', '.less']:
                    files['css_count'] += 1
                elif ext == '.json':
                    files['json_count'] += 1
                elif ext in ['.yaml', '.yml']:
                    files['yaml_count'] += 1
                elif ext == '.md':
                    files['markdown_count'] += 1
                
                # Get file stats for code files
                if ext in ['.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c']:
                    try:
                        size = file_path.stat().st_size
                        if size < 1024 * 1024:  # Less than 1MB
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                lines = len(content.split('\n'))
                                
                                files['code_file_details'].append({
                                    'path': str(file_path.relative_to(self.repo_path)),
                                    'size_kb': round(size / 1024, 2),
                                    'lines': lines,
                                    'has_content': len(content.strip()) > 50
                                })
                                
                                if size > 1024:  # Larger than 1KB
                                    files['largest_files'].append({
                                        'path': str(file_path.relative_to(self.repo_path)),
                                        'size_kb': round(size / 1024, 2),
                                        'lines': lines
                                    })
                    except:
                        continue
        
        # Sort largest files
        files['largest_files'] = sorted(files['largest_files'], 
                                      key=lambda x: x['size_kb'], 
                                      reverse=True)[:10]
        
        # Limit code file details
        files['code_file_details'] = files['code_file_details'][:20]
        
        return files
    
    def _analyze_code_quality(self) -> Dict:
        """Analyze code quality with AST parsing"""
        quality = {
            'python_metrics': self._analyze_python_code(),
            'javascript_metrics': self._analyze_javascript_code(),
            'overall': {
                'has_error_handling': False,
                'has_logging': False,
                'has_comments': False,
                'has_docstrings': False,
                'complexity_indicators': []
            }
        }
        
        # Analyze Python files
        python_files = list(self.repo_path.rglob('*.py'))
        if python_files:
            quality['python_metrics'] = self._analyze_python_files(python_files[:10])
        
        # Analyze JavaScript files
        js_files = list(self.repo_path.rglob('*.js')) + list(self.repo_path.rglob('*.jsx'))
        if js_files:
            quality['javascript_metrics'] = self._analyze_javascript_files(js_files[:5])
        
        # Check for patterns in all code files
        code_files = list(self.repo_path.rglob('*.py')) + list(self.repo_path.rglob('*.js')) + \
                    list(self.repo_path.rglob('*.jsx')) + list(self.repo_path.rglob('*.ts')) + \
                    list(self.repo_path.rglob('*.tsx'))
        
        for file_path in code_files[:15]:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Check for error handling
                    if 'try:' in content or 'except' in content or 'catch' in content:
                        quality['overall']['has_error_handling'] = True
                    
                    # Check for logging
                    if 'log' in content.lower() or 'console.' in content:
                        quality['overall']['has_logging'] = True
                    
                    # Check for comments
                    if '#' in content or '//' in content or '/*' in content:
                        quality['overall']['has_comments'] = True
                    
                    # Check for complexity
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if len(line.strip()) > 100:
                            quality['overall']['complexity_indicators'].append({
                                'file': str(file_path.relative_to(self.repo_path)),
                                'line': i + 1,
                                'issue': 'Long line (>100 chars)'
                            })
            except:
                continue
        
        # Limit complexity indicators
        quality['overall']['complexity_indicators'] = quality['overall']['complexity_indicators'][:10]
        
        return quality
    
    def _analyze_python_files(self, python_files: List[Path]) -> Dict:
        """Analyze Python files with AST"""
        metrics = {
            'total_files': len(python_files),
            'imports': [],
            'functions': [],
            'classes': [],
            'has_type_hints': False,
            'has_docstrings': False,
            'has_decorators': False
        }
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Try AST parsing
                try:
                    tree = ast.parse(content)
                    
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                metrics['imports'].append(alias.name)
                        elif isinstance(node, ast.ImportFrom):
                            module = node.module or ''
                            for alias in node.names:
                                metrics['imports'].append(f"{module}.{alias.name}")
                        
                        elif isinstance(node, ast.FunctionDef):
                            func_info = {
                                'name': node.name,
                                'has_docstring': bool(ast.get_docstring(node)),
                                'has_type_hints': bool(node.returns)
                            }
                            metrics['functions'].append(func_info)
                            
                            if func_info['has_docstring']:
                                metrics['has_docstrings'] = True
                            if func_info['has_type_hints']:
                                metrics['has_type_hints'] = True
                            if node.decorator_list:
                                metrics['has_decorators'] = True
                        
                        elif isinstance(node, ast.ClassDef):
                            class_info = {
                                'name': node.name,
                                'has_docstring': bool(ast.get_docstring(node))
                            }
                            metrics['classes'].append(class_info)
                
                except SyntaxError:
                    # Fallback to regex
                    lines = content.split('\n')
                    for line in lines:
                        if line.strip().startswith('import ') or line.strip().startswith('from '):
                            parts = line.strip().split()
                            if len(parts) > 1:
                                metrics['imports'].append(parts[1].split('.')[0])
                        elif line.strip().startswith('def '):
                            metrics['functions'].append({'name': line.strip().split()[1].split('(')[0]})
                        elif line.strip().startswith('class '):
                            metrics['classes'].append({'name': line.strip().split()[1].split('(')[0]})
            
            except:
                continue
        
        # Remove duplicates
        metrics['imports'] = list(set(metrics['imports']))
        
        return metrics
    
    def _analyze_javascript_files(self, js_files: List[Path]) -> Dict:
        """Analyze JavaScript files"""
        metrics = {
            'total_files': len(js_files),
            'imports': [],
            'functions': [],
            'classes': [],
            'has_typescript': False
        }
        
        for js_file in js_files:
            try:
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for TypeScript
                if js_file.suffix in ['.ts', '.tsx']:
                    metrics['has_typescript'] = True
                
                # Extract imports
                import_pattern = r'(import|require)\s*\(?[\'"]([^"\']+)[\'"]\)?'
                imports = re.findall(import_pattern, content)
                for imp in imports:
                    metrics['imports'].append(imp[1])
                
                # Extract functions
                function_pattern = r'function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\('
                functions = re.findall(function_pattern, content)
                metrics['functions'].extend(functions)
                
                # Extract classes
                class_pattern = r'class\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*'
                classes = re.findall(class_pattern, content)
                metrics['classes'].extend(classes)
            
            except:
                continue
        
        # Remove duplicates
        metrics['imports'] = list(set(metrics['imports']))
        metrics['functions'] = list(set(metrics['functions']))
        metrics['classes'] = list(set(metrics['classes']))
        
        return metrics
    
    def _analyze_python_code(self) -> Dict:
        """Legacy method for backward compatibility"""
        return {'total_files': 0, 'imports': [], 'functions': [], 'classes': []}
    
    def _analyze_javascript_code(self) -> Dict:
        """Legacy method for backward compatibility"""
        return {'total_files': 0, 'imports': [], 'functions': [], 'classes': []}
    
    def _analyze_dependencies(self) -> Dict:
        """Analyze dependencies"""
        deps = {
            'python': {'packages': [], 'files_found': []},
            'javascript': {'packages': [], 'files_found': []},
            'docker': {'images': [], 'files_found': []}
        }
        
        # Python dependencies
        req_files = ['requirements.txt', 'pyproject.toml', 'setup.py']
        for req_file in req_files:
            file_path = self.repo_path / req_file
            if file_path.exists():
                deps['python']['files_found'].append(req_file)
                try:
                    if req_file == 'requirements.txt':
                        with open(file_path, 'r') as f:
                            for line in f:
                                line = line.strip()
                                if line and not line.startswith('#') and not line.startswith('-'):
                                    pkg = line.split('==')[0].split('>=')[0].split('<=')[0].split('~=')[0]
                                    if pkg and pkg not in deps['python']['packages']:
                                        deps['python']['packages'].append(pkg)
                except:
                    pass
        
        # JavaScript dependencies
        package_json = self.repo_path / 'package.json'
        if package_json.exists():
            deps['javascript']['files_found'].append('package.json')
            try:
                with open(package_json, 'r') as f:
                    data = json.load(f)
                    if 'dependencies' in data:
                        deps['javascript']['packages'].extend(list(data['dependencies'].keys()))
                    if 'devDependencies' in data:
                        deps['javascript']['packages'].extend(list(data['devDependencies'].keys()))
            except:
                pass
        
        # Docker dependencies
        dockerfile = self.repo_path / 'Dockerfile'
        if dockerfile.exists():
            deps['docker']['files_found'].append('Dockerfile')
            try:
                with open(dockerfile, 'r') as f:
                    for line in f:
                        if line.strip().upper().startswith('FROM '):
                            image = line[5:].strip().split()[0]
                            if image and image not in deps['docker']['images']:
                                deps['docker']['images'].append(image)
            except:
                pass
        
        return deps
    
    def _analyze_documentation(self) -> Dict:
        """Analyze documentation"""
        docs = {
            'readme': {'exists': False, 'sections': {}, 'quality_score': 0},
            'api_docs': {'exists': False, 'files': []},
            'architecture_docs': {'exists': False, 'files': []}
        }
        
        # Find README
        readme_files = list(self.repo_path.glob('README*'))
        if readme_files:
            readme_file = readme_files[0]
            docs['readme']['exists'] = True
            
            try:
                with open(readme_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Check sections
                sections = {
                    'installation': ['install', 'setup', 'getting started'],
                    'usage': ['usage', 'example', 'demo'],
                    'api': ['api', 'endpoint', 'rest', 'graphql'],
                    'configuration': ['config', 'setting', 'environment'],
                    'testing': ['test', 'testing'],
                    'deployment': ['deploy', 'docker', 'production']
                }
                
                content_lower = content.lower()
                found_sections = {}
                for section, keywords in sections.items():
                    found_sections[section] = any(keyword in content_lower for keyword in keywords)
                
                docs['readme']['sections'] = found_sections
                
                # Calculate quality score
                score = 0
                for section in ['installation', 'usage', 'api', 'configuration', 'testing', 'deployment']:
                    if found_sections.get(section):
                        score += 1
                docs['readme']['quality_score'] = min(score, 6)
            
            except:
                pass
        
        return docs
    
    def _analyze_testing(self) -> Dict:
        """Analyze testing"""
        testing = {
            'has_tests': False,
            'test_files': [],
            'test_frameworks': set(),
            'coverage': False,
            'test_directory_structure': False
        }
        
        # Find test directory
        test_dirs = ['tests', 'test', '__tests__']
        for test_dir in test_dirs:
            if (self.repo_path / test_dir).exists():
                testing['has_tests'] = True
                testing['test_directory_structure'] = True
                
                # Find test files
                for pattern in ['*.py', '*.js', '*.ts']:
                    test_files = list((self.repo_path / test_dir).rglob(pattern))
                    for test_file in test_files:
                        if 'test' in test_file.name.lower() or 'spec' in test_file.name.lower():
                            testing['test_files'].append(str(test_file.relative_to(self.repo_path)))
                break
        
        # Also look for test files in root
        if not testing['has_tests']:
            for pattern in ['*test*.py', '*spec*.js', '*test*.js']:
                test_files = list(self.repo_path.rglob(pattern))
                for test_file in test_files:
                    if 'test' in test_file.name.lower() or 'spec' in test_file.name.lower():
                        testing['test_files'].append(str(test_file.relative_to(self.repo_path)))
                        testing['has_tests'] = True
        
        # Check for coverage files
        coverage_files = ['.coverage', 'coverage.xml', 'coverage.json']
        for file_name in coverage_files:
            if (self.repo_path / file_name).exists():
                testing['coverage'] = True
                break
        
        # Detect test frameworks from file content
        for test_file in testing['test_files'][:5]:
            try:
                with open(self.repo_path / test_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if 'pytest' in content:
                        testing['test_frameworks'].add('pytest')
                    if 'unittest' in content:
                        testing['test_frameworks'].add('unittest')
                    if 'jest' in content:
                        testing['test_frameworks'].add('jest')
                    if 'mocha' in content:
                        testing['test_frameworks'].add('mocha')
            except:
                continue
        
        testing['test_frameworks'] = list(testing['test_frameworks'])
        
        return testing
    
    def _analyze_docker(self) -> Dict:
        """Analyze Docker configuration"""
        docker = {
            'has_dockerfile': False,
            'has_docker_compose': False
        }
        
        # Check for Dockerfile
        dockerfiles = list(self.repo_path.glob('Dockerfile*'))
        if dockerfiles:
            docker['has_dockerfile'] = True
        
        # Check for docker-compose
        compose_files = list(self.repo_path.glob('docker-compose*'))
        if compose_files:
            docker['has_docker_compose'] = True
        
        return docker
    
    def _analyze_ci_cd(self) -> Dict:
        """Analyze CI/CD configuration"""
        ci_cd = {
            'has_ci': False,
            'ci_files': [],
            'ci_platforms': set()
        }
        
        # Check for CI files
        ci_patterns = ['.github/workflows/*.yml', '.github/workflows/*.yaml', 
                      '.gitlab-ci.yml', '.travis.yml']
        
        for pattern in ci_patterns:
            ci_files = list(self.repo_path.rglob(pattern))
            if ci_files:
                ci_cd['has_ci'] = True
                ci_cd['ci_files'].extend([
                    str(f.relative_to(self.repo_path)) for f in ci_files
                ])
                
                for ci_file in ci_files:
                    rel_path = str(ci_file.relative_to(self.repo_path))
                    if 'github' in rel_path:
                        ci_cd['ci_platforms'].add('GitHub Actions')
                    elif 'gitlab' in rel_path:
                        ci_cd['ci_platforms'].add('GitLab CI')
                    elif 'travis' in rel_path:
                        ci_cd['ci_platforms'].add('Travis CI')
        
        ci_cd['ci_platforms'] = list(ci_cd['ci_platforms'])
        
        return ci_cd
    
    def _analyze_challenge_specific(self) -> Dict:
        """Analyze challenge-specific indicators"""
        challenge_specific = {
            'ai_ml_indicators': {
                'has_ai_ml': False,
                'libraries': []
            },
            'web_app_indicators': {
                'has_web_app': False
            },
            'data_pipeline_indicators': {
                'has_data_pipeline': False
            }
        }
        
        # Check for AI/ML libraries in Python files
        ai_ml_libraries = ['tensorflow', 'torch', 'pytorch', 'transformers', 'langchain', 
                          'opencv', 'pytesseract', 'easyocr', 'yolo']
        
        python_files = list(self.repo_path.rglob('*.py'))
        for py_file in python_files[:5]:
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()
                    for lib in ai_ml_libraries:
                        if lib in content:
                            challenge_specific['ai_ml_indicators']['has_ai_ml'] = True
                            if lib not in challenge_specific['ai_ml_indicators']['libraries']:
                                challenge_specific['ai_ml_indicators']['libraries'].append(lib)
            except:
                continue
        
        # Check for web app indicators
        web_files = list(self.repo_path.rglob('*.html')) + list(self.repo_path.rglob('*.js')) + \
                   list(self.repo_path.rglob('*.jsx'))
        if web_files:
            challenge_specific['web_app_indicators']['has_web_app'] = True
        
        # Check for data pipeline indicators
        data_files = list(self.repo_path.rglob('*.sql')) + list(self.repo_path.rglob('*etl*')) + \
                    list(self.repo_path.rglob('*pipeline*'))
        if data_files:
            challenge_specific['data_pipeline_indicators']['has_data_pipeline'] = True
        
        return challenge_specific
    
    def _extract_key_files(self) -> Dict:
        """Extract content from key files"""
        key_files = {
            'readme': '',
            'requirements': '',
            'dockerfile': '',
            'main_app': ''
        }
        
        # Read README
        readme_files = list(self.repo_path.glob('README*'))
        if readme_files:
            try:
                with open(readme_files[0], 'r', encoding='utf-8', errors='ignore') as f:
                    key_files['readme'] = f.read(2000)
            except:
                pass
        
        # Read requirements
        req_files = ['requirements.txt', 'package.json']
        for file_name in req_files:
            file_path = self.repo_path / file_name
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        key_files['requirements'] += f"\n=== {file_name} ===\n" + f.read(1000)
                except:
                    pass
        
        # Read Dockerfile
        dockerfile = self.repo_path / 'Dockerfile'
        if dockerfile.exists():
            try:
                with open(dockerfile, 'r') as f:
                    key_files['dockerfile'] = f.read(1000)
            except:
                pass
        
        # Find main application file
        main_patterns = ['main.py', 'app.py', 'index.js', 'server.js']
        for pattern in main_patterns:
            main_files = list(self.repo_path.rglob(pattern))
            if main_files:
                try:
                    with open(main_files[0], 'r', encoding='utf-8') as f:
                        key_files['main_app'] = f.read(2000)
                    break
                except:
                    continue
        
        return key_files
    
    def _calculate_stats(self) -> Dict:
        """Calculate repository statistics"""
        stats = {
            'file_count': 0,
            'line_count': 0,
            'code_files': 0,
            'comment_lines': 0,
            'blank_lines': 0
        }
        
        code_extensions = {'.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c'}
        
        for root, dirs, files in os.walk(self.repo_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                if file.startswith('.'):
                    continue
                
                file_path = Path(root) / file
                stats['file_count'] += 1
                
                # Count lines for code files
                if file_path.suffix in code_extensions:
                    stats['code_files'] += 1
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()
                            stats['line_count'] += len(lines)
                            
                            for line in lines:
                                line_stripped = line.strip()
                                if not line_stripped:
                                    stats['blank_lines'] += 1
                                elif line_stripped.startswith('#') or line_stripped.startswith('//'):
                                    stats['comment_lines'] += 1
                    except:
                        continue
        
        return stats
    
    def _analyze_code_patterns(self) -> Dict:
        """Analyze code patterns"""
        patterns_found = {
            'error_handling': [],
            'logging': [],
            'testing': []
        }
        
        code_files = list(self.repo_path.rglob('*.py')) + list(self.repo_path.rglob('*.js')) + \
                    list(self.repo_path.rglob('*.ts'))
        
        for file_path in code_files[:10]:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    rel_path = str(file_path.relative_to(self.repo_path))
                    
                    # Error handling patterns
                    if 'try:' in content or 'except' in content or 'catch' in content:
                        patterns_found['error_handling'].append({
                            'file': rel_path,
                            'count': content.count('try:') + content.count('except') + content.count('catch')
                        })
                    
                    # Logging patterns
                    if 'log' in content.lower() or 'console.' in content:
                        patterns_found['logging'].append({
                            'file': rel_path,
                            'count': content.lower().count('log')
                        })
                    
                    # Testing patterns
                    if 'test' in content.lower() or 'assert' in content:
                        patterns_found['testing'].append({
                            'file': rel_path,
                            'count': content.lower().count('test') + content.count('assert')
                        })
                        
            except:
                continue
        
        return patterns_found