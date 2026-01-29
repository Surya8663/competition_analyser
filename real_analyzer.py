# real_analyzer.py - 100% REAL DEEP REPOSITORY ANALYSIS
import os
import json
import re
import ast
import yaml
import toml
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
import subprocess

class RealRepositoryAnalyzer:
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.analysis = {}
        
    def analyze_deep(self) -> Dict:
        """DEEP analysis - reads files, understands code, extracts REAL data"""
        try:
            return {
                'metadata': self._analyze_metadata(),
                'structure': self._analyze_structure_deep(),
                'files': self._analyze_files_deep(),
                'code_quality': self._analyze_code_quality(),
                'dependencies': self._analyze_dependencies_deep(),
                'documentation': self._analyze_documentation_deep(),
                'testing': self._analyze_testing(),
                'docker': self._analyze_docker(),
                'ci_cd': self._analyze_ci_cd(),
                'challenge_specific': self._analyze_challenge_specific(),
                'key_files_content': self._extract_key_files(),
                'stats': self._calculate_stats()
            }
        except Exception as e:
            return {'error': f"Deep analysis error: {str(e)}"}
    
    def _analyze_metadata(self) -> Dict:
        """Extract repository metadata"""
        metadata = {
            'has_readme': False,
            'has_license': False,
            'has_gitignore': False,
            'total_files': 0,
            'total_lines': 0,
            'repo_size_mb': 0
        }
        
        # Count files and lines
        total_files = 0
        total_lines = 0
        for root, dirs, files in os.walk(self.repo_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                if file.startswith('.'):
                    continue
                file_path = Path(root) / file
                try:
                    total_files += 1
                    if file_path.suffix in ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs', '.rb']:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            total_lines += len(f.readlines())
                except:
                    continue
        
        metadata['total_files'] = total_files
        metadata['total_lines'] = total_lines
        
        # Check for key files
        key_files = ['README.md', 'README.rst', 'README.txt']
        for f in key_files:
            if (self.repo_path / f).exists():
                metadata['has_readme'] = True
                break
        
        metadata['has_license'] = any((self.repo_path / f).exists() 
                                    for f in ['LICENSE', 'LICENSE.txt', 'LICENSE.md'])
        metadata['has_gitignore'] = (self.repo_path / '.gitignore').exists()
        
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
    
    def _analyze_structure_deep(self) -> Dict:
        """Deep structure analysis"""
        structure = {
            'directory_tree': {},
            'tech_stack_indicators': {},
            'architecture_patterns': []
        }
        
        # Build directory tree
        for root, dirs, files in os.walk(self.repo_path, topdown=True):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            rel_path = Path(root).relative_to(self.repo_path)
            rel_path_str = str(rel_path) if str(rel_path) != '.' else '/'
            
            structure['directory_tree'][rel_path_str] = {
                'directories': dirs.copy(),
                'files': [f for f in files if not f.startswith('.')],
                'file_count': len([f for f in files if not f.startswith('.')])
            }
            
            # Detect tech stack from directories
            for dir_name in dirs:
                dir_lower = dir_name.lower()
                if dir_lower in ['src', 'app', 'lib', 'core']:
                    structure['tech_stack_indicators']['backend'] = True
                elif dir_lower in ['frontend', 'client', 'web', 'public', 'static']:
                    structure['tech_stack_indicators']['frontend'] = True
                elif dir_lower in ['tests', 'test', '__tests__']:
                    structure['tech_stack_indicators']['testing'] = True
                elif dir_lower in ['docs', 'documentation']:
                    structure['tech_stack_indicators']['documentation'] = True
                elif dir_lower in ['docker', 'deploy', 'infrastructure']:
                    structure['tech_stack_indicators']['deployment'] = True
                elif dir_lower in ['config', 'configuration', 'settings']:
                    structure['tech_stack_indicators']['configuration'] = True
        
        # Detect architecture patterns
        if 'src' in [d.lower() for d in structure['directory_tree'].get('/', {}).get('directories', [])]:
            structure['architecture_patterns'].append('src-based')
        if 'app' in [d.lower() for d in structure['directory_tree'].get('/', {}).get('directories', [])]:
            structure['architecture_patterns'].append('app-based')
        if 'tests' in [d.lower() for d in structure['directory_tree'].get('/', {}).get('directories', [])]:
            structure['architecture_patterns'].append('test-separated')
        
        return structure
    
    def _analyze_files_deep(self) -> Dict:
        """Deep file analysis"""
        files_analysis = {
            'by_extension': {},
            'by_language': {},
            'largest_files': [],
            'most_complex_files': []
        }
        
        file_stats = []
        
        for root, dirs, files in os.walk(self.repo_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                if file.startswith('.'):
                    continue
                
                file_path = Path(root) / file
                rel_path = file_path.relative_to(self.repo_path)
                ext = file_path.suffix.lower()
                
                # Count by extension
                files_analysis['by_extension'][ext] = files_analysis['by_extension'].get(ext, 0) + 1
                
                # Classify by language
                lang = self._classify_language(ext, file_path.name)
                if lang:
                    files_analysis['by_language'][lang] = files_analysis['by_language'].get(lang, 0) + 1
                
                try:
                    # Get file stats
                    size = file_path.stat().st_size
                    if size < 1024 * 1024:  # Skip files larger than 1MB for content analysis
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            lines = content.count('\n') + 1
                            
                            file_stats.append({
                                'path': str(rel_path),
                                'size_bytes': size,
                                'lines': lines,
                                'language': lang,
                                'extension': ext
                            })
                            
                            # Find largest files
                            if size > 1024:  # Larger than 1KB
                                files_analysis['largest_files'].append({
                                    'path': str(rel_path),
                                    'size_kb': round(size / 1024, 2),
                                    'lines': lines
                                })
                except:
                    continue
        
        # Sort and limit
        files_analysis['largest_files'] = sorted(
            files_analysis['largest_files'], 
            key=lambda x: x['size_kb'], 
            reverse=True
        )[:10]
        
        return files_analysis
    
    def _classify_language(self, ext: str, filename: str) -> str:
        """Classify file by programming language"""
        language_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.jsx': 'JavaScript (React)',
            '.ts': 'TypeScript',
            '.tsx': 'TypeScript (React)',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.go': 'Go',
            '.rs': 'Rust',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.html': 'HTML',
            '.css': 'CSS',
            '.scss': 'SCSS',
            '.less': 'LESS',
            '.json': 'JSON',
            '.yaml': 'YAML',
            '.yml': 'YAML',
            '.toml': 'TOML',
            '.md': 'Markdown',
            '.sql': 'SQL',
            '.sh': 'Shell',
            '.dockerfile': 'Docker',
            'dockerfile': 'Docker',
            '.ipynb': 'Jupyter Notebook'
        }
        
        if ext in language_map:
            return language_map[ext]
        elif filename.lower() == 'dockerfile':
            return 'Docker'
        return 'Other'
    
    def _analyze_code_quality(self) -> Dict:
        """Analyze code quality metrics"""
        quality = {
            'python_metrics': {},
            'javascript_metrics': {},
            'overall': {
                'has_error_handling': False,
                'has_logging': False,
                'has_comments': False,
                'has_docstrings': False,
                'complex_files': []
            }
        }
        
        # Analyze Python files
        python_files = list(self.repo_path.rglob('*.py'))
        if python_files:
            py_metrics = self._analyze_python_code(python_files[:20])  # Analyze first 20 files
            quality['python_metrics'] = py_metrics
        
        # Analyze JavaScript files
        js_files = list(self.repo_path.rglob('*.js')) + list(self.repo_path.rglob('*.jsx'))
        if js_files:
            js_metrics = self._analyze_javascript_code(js_files[:20])
            quality['javascript_metrics'] = js_metrics
        
        # Check for error handling patterns
        error_patterns = ['try:', 'except', 'catch', 'finally', 'throw', 'raise']
        for root, dirs, files in os.walk(self.repo_path):
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.java')):
                    file_path = Path(root) / file
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if any(pattern in content for pattern in error_patterns):
                                quality['overall']['has_error_handling'] = True
                            if 'log' in content.lower() or 'console.' in content:
                                quality['overall']['has_logging'] = True
                            if '#' in content or '//' in content or '/*' in content:
                                quality['overall']['has_comments'] = True
                    except:
                        continue
        
        return quality
    
    def _analyze_python_code(self, python_files: List[Path]) -> Dict:
        """Deep analysis of Python code"""
        metrics = {
            'total_files': len(python_files),
            'imports': set(),
            'functions': 0,
            'classes': 0,
            'async_functions': 0,
            'has_type_hints': False,
            'has_docstrings': False,
            'avg_lines_per_file': 0,
            'complexity_scores': []
        }
        
        total_lines = 0
        for py_file in python_files[:10]:  # Analyze first 10 files in detail
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    total_lines += len(lines)
                    
                    # Parse with AST
                    try:
                        tree = ast.parse(content)
                        
                        # Count functions and classes
                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef):
                                metrics['functions'] += 1
                                if node.name.startswith('async'):
                                    metrics['async_functions'] += 1
                                if ast.get_docstring(node):
                                    metrics['has_docstrings'] = True
                                if node.returns:
                                    metrics['has_type_hints'] = True
                            elif isinstance(node, ast.ClassDef):
                                metrics['classes'] += 1
                            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                                if isinstance(node, ast.Import):
                                    for alias in node.names:
                                        metrics['imports'].add(alias.name)
                                elif isinstance(node, ast.ImportFrom):
                                    metrics['imports'].add(node.module or '')
                    except SyntaxError:
                        # Fallback to simple analysis
                        for line in lines:
                            if line.strip().startswith('import ') or line.strip().startswith('from '):
                                parts = line.strip().split()
                                if len(parts) > 1:
                                    metrics['imports'].add(parts[1].split('.')[0])
                            if line.strip().startswith('def '):
                                metrics['functions'] += 1
                            if line.strip().startswith('class '):
                                metrics['classes'] += 1
                    
                    # Calculate basic complexity (line count + nesting)
                    complexity = self._calculate_python_complexity(content)
                    if complexity > 50:  # Arbitrary threshold
                        metrics['complexity_scores'].append({
                            'file': str(py_file.relative_to(self.repo_path)),
                            'complexity': complexity,
                            'lines': len(lines)
                        })
            except:
                continue
        
        if metrics['total_files'] > 0:
            metrics['avg_lines_per_file'] = total_lines / metrics['total_files']
        
        # Convert imports set to list
        metrics['imports'] = list(metrics['imports'])[:20]  # Limit to 20
        
        return metrics
    
    def _analyze_javascript_code(self, js_files: List[Path]) -> Dict:
        """Deep analysis of JavaScript/TypeScript code"""
        metrics = {
            'total_files': len(js_files),
            'imports': set(),
            'exports': set(),
            'functions': 0,
            'classes': 0,
            'has_types': False,
            'has_jsdoc': False,
            'avg_lines_per_file': 0
        }
        
        total_lines = 0
        for js_file in js_files[:10]:
            try:
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    total_lines += len(lines)
                    
                    for line in lines:
                        line = line.strip()
                        # Check imports
                        if line.startswith('import ') or line.startswith('require('):
                            metrics['imports'].add(line)
                        # Check exports
                        if line.startswith('export '):
                            metrics['exports'].add(line)
                        # Check for TypeScript
                        if ': ' in line and ('string' in line or 'number' in line or 'boolean' in line):
                            metrics['has_types'] = True
                        # Check for JSDoc
                        if '/**' in line or '* @' in line:
                            metrics['has_jsdoc'] = True
                        # Count functions
                        if 'function ' in line or '=>' in line:
                            metrics['functions'] += 1
                        # Count classes
                        if 'class ' in line:
                            metrics['classes'] += 1
            except:
                continue
        
        if metrics['total_files'] > 0:
            metrics['avg_lines_per_file'] = total_lines / metrics['total_files']
        
        metrics['imports'] = list(metrics['imports'])[:20]
        metrics['exports'] = list(metrics['exports'])[:10]
        
        return metrics
    
    def _calculate_python_complexity(self, content: str) -> int:
        """Calculate simple complexity score for Python"""
        lines = content.split('\n')
        complexity = len(lines)
        
        # Add points for nested structures
        for line in lines:
            indentation = len(line) - len(line.lstrip())
            if indentation > 12:  # 3 levels deep (4 spaces each * 3)
                complexity += 1
            if 'if ' in line and ' and ' in line:
                complexity += 1
            if 'for ' in line and ' in ' in line:
                complexity += 1
            if 'while ' in line:
                complexity += 1
        
        return complexity
    
    def _analyze_dependencies_deep(self) -> Dict:
        """Deep dependency analysis"""
        dependencies = {
            'python': {'packages': [], 'files_found': []},
            'javascript': {'packages': [], 'files_found': []},
            'docker': {'images': [], 'files_found': []},
            'system': {'tools': [], 'files_found': []}
        }
        
        # Python dependencies
        py_files = ['requirements.txt', 'pyproject.toml', 'setup.py', 'Pipfile', 'setup.cfg']
        for file_name in py_files:
            file_path = self.repo_path / file_name
            if file_path.exists():
                dependencies['python']['files_found'].append(file_name)
                try:
                    if file_name == 'requirements.txt':
                        deps = self._parse_requirements_txt(file_path)
                        dependencies['python']['packages'].extend(deps)
                    elif file_name == 'pyproject.toml':
                        deps = self._parse_pyproject_toml(file_path)
                        dependencies['python']['packages'].extend(deps)
                    elif file_name == 'setup.py':
                        deps = self._parse_setup_py(file_path)
                        dependencies['python']['packages'].extend(deps)
                except:
                    continue
        
        # JavaScript dependencies
        js_files = ['package.json', 'yarn.lock', 'package-lock.json']
        for file_name in js_files:
            file_path = self.repo_path / file_name
            if file_path.exists():
                dependencies['javascript']['files_found'].append(file_name)
                try:
                    if file_name == 'package.json':
                        deps = self._parse_package_json(file_path)
                        dependencies['javascript']['packages'].extend(deps)
                except:
                    continue
        
        # Docker dependencies
        docker_files = ['Dockerfile', 'docker-compose.yml', 'docker-compose.yaml']
        for file_name in docker_files:
            file_path = self.repo_path / file_name
            if file_path.exists():
                dependencies['docker']['files_found'].append(file_name)
                try:
                    if file_name.startswith('Dockerfile'):
                        images = self._parse_dockerfile(file_path)
                        dependencies['docker']['images'].extend(images)
                except:
                    continue
        
        # Remove duplicates
        for lang in dependencies:
            if 'packages' in dependencies[lang]:
                dependencies[lang]['packages'] = list(set(dependencies[lang]['packages']))
            if 'images' in dependencies[lang]:
                dependencies[lang]['images'] = list(set(dependencies[lang]['images']))
        
        return dependencies
    
    def _parse_requirements_txt(self, file_path: Path) -> List[str]:
        """Parse requirements.txt"""
        packages = []
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and not line.startswith('-'):
                        # Extract package name (remove versions)
                        package = line.split('==')[0].split('>=')[0].split('<=')[0].split('~=')[0]
                        if package and package not in packages:
                            packages.append(package)
        except:
            pass
        return packages
    
    def _parse_pyproject_toml(self, file_path: Path) -> List[str]:
        """Parse pyproject.toml"""
        packages = []
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                # Simple regex extraction
                import re
                # Look for dependencies sections
                deps_sections = re.findall(r'\[tool\.poetry\.dependencies\](.*?)(?=\[|\Z)', content, re.DOTALL)
                for section in deps_sections:
                    lines = section.strip().split('\n')
                    for line in lines:
                        line = line.strip()
                        if '=' in line and not line.startswith('#'):
                            package = line.split('=')[0].strip().strip('"').strip("'")
                            if package and package not in packages and package != 'python':
                                packages.append(package)
        except:
            pass
        return packages
    
    def _parse_setup_py(self, file_path: Path) -> List[str]:
        """Parse setup.py"""
        packages = []
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                # Look for install_requires
                import re
                matches = re.findall(r'install_requires\s*=\s*\[(.*?)\]', content, re.DOTALL)
                for match in matches:
                    lines = match.split('\n')
                    for line in lines:
                        line = line.strip().strip(',').strip("'").strip('"')
                        if line and not line.startswith('#') and line not in packages:
                            packages.append(line)
        except:
            pass
        return packages
    
    def _parse_package_json(self, file_path: Path) -> List[str]:
        """Parse package.json"""
        packages = []
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                if 'dependencies' in data:
                    packages.extend(list(data['dependencies'].keys()))
                if 'devDependencies' in data:
                    packages.extend(list(data['devDependencies'].keys()))
        except:
            pass
        return packages
    
    def _parse_dockerfile(self, file_path: Path) -> List[str]:
        """Parse Dockerfile for base images"""
        images = []
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.upper().startswith('FROM '):
                        image = line[5:].strip().split()[0]  # Get the image name
                        if image and image not in images:
                            images.append(image)
        except:
            pass
        return images
    
    def _analyze_documentation_deep(self) -> Dict:
        """Deep documentation analysis"""
        docs = {
            'readme': {'exists': False, 'sections': {}, 'quality_score': 0},
            'api_docs': {'exists': False, 'files': []},
            'architecture_docs': {'exists': False, 'files': []},
            'setup_instructions': {'exists': False, 'clarity': 0},
            'examples': {'exists': False, 'count': 0}
        }
        
        # Find and analyze README
        readme_files = list(self.repo_path.glob('README*'))
        if readme_files:
            readme_file = readme_files[0]
            docs['readme']['exists'] = True
            
            try:
                with open(readme_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    docs['readme']['content_preview'] = content[:1000] + "..." if len(content) > 1000 else content
                    
                    # Analyze README sections
                    sections = {
                        'installation': ['install', 'setup', 'getting started'],
                        'usage': ['usage', 'example', 'demo'],
                        'api': ['api', 'endpoint', 'rest', 'graphql'],
                        'configuration': ['config', 'setting', 'environment'],
                        'testing': ['test', 'testing'],
                        'deployment': ['deploy', 'docker', 'production'],
                        'contributing': ['contribut', 'develop'],
                        'license': ['license', 'licence']
                    }
                    
                    content_lower = content.lower()
                    found_sections = {}
                    for section, keywords in sections.items():
                        found_sections[section] = any(keyword in content_lower for keyword in keywords)
                    
                    docs['readme']['sections'] = found_sections
                    
                    # Calculate quality score (0-10)
                    score = 0
                    if found_sections.get('installation'): score += 2
                    if found_sections.get('usage'): score += 2
                    if found_sections.get('api'): score += 1
                    if found_sections.get('configuration'): score += 1
                    if found_sections.get('testing'): score += 1
                    if found_sections.get('deployment'): score += 1
                    if found_sections.get('contributing'): score += 1
                    if found_sections.get('license'): score += 1
                    
                    docs['readme']['quality_score'] = min(score, 10)
                    
                    # Check for setup instructions
                    if found_sections.get('installation'):
                        docs['setup_instructions']['exists'] = True
                        # Check clarity (has code blocks)
                        if '```' in content or '`' in content:
                            docs['setup_instructions']['clarity'] = 2
                        elif 'pip install' in content_lower or 'npm install' in content_lower:
                            docs['setup_instructions']['clarity'] = 1
                    
                    # Check for examples
                    if found_sections.get('usage'):
                        docs['examples']['exists'] = True
                        # Count example code blocks
                        code_blocks = content.count('```')
                        docs['examples']['count'] = code_blocks // 2  # Each block has opening and closing
            except:
                pass
        
        # Look for API documentation
        api_doc_patterns = ['api.md', 'docs/api', 'swagger', 'openapi']
        for pattern in api_doc_patterns:
            for path in self.repo_path.rglob(pattern):
                if path.is_file():
                    docs['api_docs']['exists'] = True
                    docs['api_docs']['files'].append(str(path.relative_to(self.repo_path)))
        
        # Look for architecture docs
        arch_patterns = ['architecture.md', 'docs/arch', 'design.md']
        for pattern in arch_patterns:
            for path in self.repo_path.rglob(pattern):
                if path.is_file():
                    docs['architecture_docs']['exists'] = True
                    docs['architecture_docs']['files'].append(str(path.relative_to(self.repo_path)))
        
        return docs
    
    def _analyze_testing(self) -> Dict:
        """Analyze testing setup"""
        testing = {
            'has_tests': False,
            'test_files': [],
            'test_frameworks': set(),
            'coverage': False,
            'test_directory_structure': False
        }
        
        # Find test files
        test_patterns = ['*test*.py', '*spec*.js', '*test*.js', '*test*.ts', '*test*.java']
        for pattern in test_patterns:
            test_files = list(self.repo_path.rglob(pattern))
            for test_file in test_files:
                rel_path = str(test_file.relative_to(self.repo_path))
                if 'node_modules' not in rel_path and '__pycache__' not in rel_path:
                    testing['test_files'].append(rel_path)
        
        testing['has_tests'] = len(testing['test_files']) > 0
        
        # Detect test frameworks
        for test_file in testing['test_files'][:10]:  # Check first 10 test files
            test_path = self.repo_path / test_file
            try:
                with open(test_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if 'pytest' in content or '@pytest' in content:
                        testing['test_frameworks'].add('pytest')
                    if 'unittest' in content:
                        testing['test_frameworks'].add('unittest')
                    if 'jest' in content or 'describe(' in content or 'it(' in content:
                        testing['test_frameworks'].add('jest')
                    if 'mocha' in content:
                        testing['test_frameworks'].add('mocha')
                    if 'junit' in content.lower():
                        testing['test_frameworks'].add('junit')
            except:
                continue
        
        # Check for coverage files
        coverage_files = ['.coverage', 'coverage.xml', 'coverage.json', 'lcov.info']
        for file_name in coverage_files:
            if (self.repo_path / file_name).exists():
                testing['coverage'] = True
                break
        
        # Check test directory structure
        test_dirs = ['tests', 'test', '__tests__', 'spec']
        for dir_name in test_dirs:
            if (self.repo_path / dir_name).exists():
                testing['test_directory_structure'] = True
                break
        
        testing['test_frameworks'] = list(testing['test_frameworks'])
        
        return testing
    
    def _analyze_docker(self) -> Dict:
        """Analyze Docker configuration"""
        docker = {
            'has_dockerfile': False,
            'has_docker_compose': False,
            'dockerfile_analysis': {},
            'multi_stage': False,
            'optimized': False
        }
        
        # Check for Dockerfile
        dockerfiles = list(self.repo_path.glob('Dockerfile*'))
        if dockerfiles:
            dockerfile = dockerfiles[0]
            docker['has_dockerfile'] = True
            
            try:
                with open(dockerfile, 'r') as f:
                    content = f.read()
                    
                    docker['dockerfile_analysis'] = {
                        'lines': len(content.split('\n')),
                        'base_images': [],
                        'multi_stage': content.count('FROM ') > 1,
                        'has_healthcheck': 'HEALTHCHECK' in content,
                        'has_non_root_user': 'USER ' in content and 'root' not in content,
                        'has_optimizations': any(x in content for x in ['--no-cache', '--no-install-recommends', 'alpine'])
                    }
                    
                    # Extract base images
                    for line in content.split('\n'):
                        if line.strip().upper().startswith('FROM '):
                            image = line[5:].strip().split()[0]
                            if image and image not in docker['dockerfile_analysis']['base_images']:
                                docker['dockerfile_analysis']['base_images'].append(image)
                    
                    docker['multi_stage'] = docker['dockerfile_analysis']['multi_stage']
                    docker['optimized'] = docker['dockerfile_analysis']['has_optimizations']
            except:
                pass
        
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
            'ci_platforms': set(),
            'has_cd': False,
            'deployment_files': []
        }
        
        # Check for CI files
        ci_patterns = [
            '.github/workflows/*.yml',
            '.github/workflows/*.yaml',
            '.gitlab-ci.yml',
            '.travis.yml',
            'circle.yml',
            'Jenkinsfile',
            '.azure-pipelines.yml'
        ]
        
        for pattern in ci_patterns:
            ci_files = list(self.repo_path.rglob(pattern))
            if ci_files:
                ci_cd['has_ci'] = True
                for ci_file in ci_files:
                    rel_path = str(ci_file.relative_to(self.repo_path))
                    ci_cd['ci_files'].append(rel_path)
                    
                    # Detect platform
                    if 'github' in rel_path:
                        ci_cd['ci_platforms'].add('GitHub Actions')
                    elif 'gitlab' in rel_path:
                        ci_cd['ci_platforms'].add('GitLab CI')
                    elif 'travis' in rel_path:
                        ci_cd['ci_platforms'].add('Travis CI')
                    elif 'circle' in rel_path:
                        ci_cd['ci_platforms'].add('CircleCI')
                    elif 'jenkins' in rel_path.lower():
                        ci_cd['ci_platforms'].add('Jenkins')
                    elif 'azure' in rel_path:
                        ci_cd['ci_platforms'].add('Azure DevOps')
        
        ci_cd['ci_platforms'] = list(ci_cd['ci_platforms'])
        
        return ci_cd
    
    def _analyze_challenge_specific(self) -> Dict:
        """Analyze specific to coding challenges"""
        challenge_specific = {
            'ai_ml_indicators': {
                'has_ai_ml': False,
                'libraries': [],
                'model_files': [],
                'notebooks': []
            },
            'web_app_indicators': {
                'has_web_app': False,
                'frameworks': [],
                'static_files': [],
                'templates': []
            },
            'data_pipeline_indicators': {
                'has_data_pipeline': False,
                'etl_files': [],
                'database_files': [],
                'airflow_files': []
            }
        }
        
        # AI/ML indicators
        ai_ml_libraries = ['tensorflow', 'torch', 'pytorch', 'transformers', 'langchain', 'openai', 
                          'langgraph', 'crewai', 'autogen', 'llamaindex', 'haystack', 'chromadb']
        
        # Check Python files for AI/ML imports
        python_files = list(self.repo_path.rglob('*.py'))
        for py_file in python_files[:20]:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    for lib in ai_ml_libraries:
                        if lib in content:
                            challenge_specific['ai_ml_indicators']['has_ai_ml'] = True
                            if lib not in challenge_specific['ai_ml_indicators']['libraries']:
                                challenge_specific['ai_ml_indicators']['libraries'].append(lib)
            except:
                continue
        
        # Look for model files
        model_patterns = ['*.pth', '*.pt', '*.h5', '*.keras', '*.joblib', '*.pkl']
        for pattern in model_patterns:
            model_files = list(self.repo_path.rglob(pattern))
            for model_file in model_files:
                rel_path = str(model_file.relative_to(self.repo_path))
                challenge_specific['ai_ml_indicators']['model_files'].append(rel_path)
        
        # Look for notebooks
        notebook_files = list(self.repo_path.rglob('*.ipynb'))
        if notebook_files:
            challenge_specific['ai_ml_indicators']['has_ai_ml'] = True
            for nb_file in notebook_files:
                challenge_specific['ai_ml_indicators']['notebooks'].append(
                    str(nb_file.relative_to(self.repo_path))
                )
        
        # Web app indicators
        web_frameworks = ['flask', 'django', 'fastapi', 'streamlit', 'gradio', 'react', 'vue', 'angular']
        static_dirs = ['static', 'public', 'assets', 'dist', 'build']
        template_dirs = ['templates', 'views', 'pages']
        
        # Check for web framework files
        for framework in web_frameworks:
            framework_files = list(self.repo_path.rglob(f'*{framework}*'))
            if framework_files:
                challenge_specific['web_app_indicators']['has_web_app'] = True
                if framework not in challenge_specific['web_app_indicators']['frameworks']:
                    challenge_specific['web_app_indicators']['frameworks'].append(framework)
        
        # Check for static and template directories
        for dir_name in static_dirs:
            if (self.repo_path / dir_name).exists():
                challenge_specific['web_app_indicators']['has_web_app'] = True
                challenge_specific['web_app_indicators']['static_files'].append(dir_name)
        
        for dir_name in template_dirs:
            if (self.repo_path / dir_name).exists():
                challenge_specific['web_app_indicators']['has_web_app'] = True
                challenge_specific['web_app_indicators']['templates'].append(dir_name)
        
        # Data pipeline indicators
        etl_patterns = ['etl', 'pipeline', 'ingest', 'transform', 'load']
        database_files = ['*.sql', 'schema.*', 'migration*']
        airflow_files = ['dag.py', 'airflow.cfg', 'dags/']
        
        # Check for ETL patterns in file names
        for root, dirs, files in os.walk(self.repo_path):
            for file in files:
                file_lower = file.lower()
                if any(pattern in file_lower for pattern in etl_patterns):
                    challenge_specific['data_pipeline_indicators']['has_data_pipeline'] = True
                    challenge_specific['data_pipeline_indicators']['etl_files'].append(
                        str((Path(root) / file).relative_to(self.repo_path))
                    )
        
        return challenge_specific
    
    def _extract_key_files(self) -> Dict:
        """Extract content from key files"""
        key_files = {
            'readme': '',
            'requirements': '',
            'dockerfile': '',
            'main_app': '',
            'config_files': {}
        }
        
        # Read README
        readme_files = list(self.repo_path.glob('README*'))
        if readme_files:
            try:
                with open(readme_files[0], 'r', encoding='utf-8', errors='ignore') as f:
                    key_files['readme'] = f.read(5000)  # First 5000 chars
            except:
                pass
        
        # Read requirements files
        req_files = ['requirements.txt', 'pyproject.toml', 'package.json']
        for file_name in req_files:
            file_path = self.repo_path / file_name
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        key_files['requirements'] += f"\n=== {file_name} ===\n" + f.read(2000)
                except:
                    pass
        
        # Read Dockerfile
        dockerfile = self.repo_path / 'Dockerfile'
        if dockerfile.exists():
            try:
                with open(dockerfile, 'r') as f:
                    key_files['dockerfile'] = f.read(2000)
            except:
                pass
        
        # Find and read main application files
        main_patterns = ['main.py', 'app.py', 'index.js', 'server.js', 'app.js', 'src/main/']
        for pattern in main_patterns:
            main_files = list(self.repo_path.rglob(pattern))
            if main_files:
                try:
                    with open(main_files[0], 'r', encoding='utf-8') as f:
                        key_files['main_app'] = f.read(3000)
                    break
                except:
                    continue
        
        # Read config files
        config_patterns = ['.env', 'config.*', 'settings.*', '*.cfg', '*.ini']
        for pattern in config_patterns:
            config_files = list(self.repo_path.rglob(pattern))
            for config_file in config_files[:3]:  # Read first 3 config files
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        content = f.read(1000)
                        rel_path = str(config_file.relative_to(self.repo_path))
                        key_files['config_files'][rel_path] = content
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
            'blank_lines': 0,
            'avg_file_size': 0,
            'largest_file': {'path': '', 'size_kb': 0}
        }
        
        total_size = 0
        largest_file = {'path': '', 'size': 0}
        
        code_extensions = {'.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c', '.go', '.rs', '.rb', '.php'}
        
        for root, dirs, files in os.walk(self.repo_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                if file.startswith('.'):
                    continue
                
                file_path = Path(root) / file
                try:
                    size = file_path.stat().st_size
                    total_size += size
                    stats['file_count'] += 1
                    
                    # Track largest file
                    if size > largest_file['size']:
                        largest_file = {
                            'path': str(file_path.relative_to(self.repo_path)),
                            'size': size
                        }
                    
                    # Count lines for code files
                    if file_path.suffix in code_extensions:
                        stats['code_files'] += 1
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                lines = f.readlines()
                                stats['line_count'] += len(lines)
                                
                                # Count comments and blank lines
                                for line in lines:
                                    line_stripped = line.strip()
                                    if not line_stripped:
                                        stats['blank_lines'] += 1
                                    elif line_stripped.startswith('#') or line_stripped.startswith('//'):
                                        stats['comment_lines'] += 1
                        except:
                            continue
                except:
                    continue
        
        if stats['file_count'] > 0:
            stats['avg_file_size'] = round(total_size / stats['file_count'] / 1024, 2)
        
        if largest_file['path']:
            stats['largest_file'] = {
                'path': largest_file['path'],
                'size_kb': round(largest_file['size'] / 1024, 2)
            }
        
        return stats