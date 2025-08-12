"""
Quantum-Enhanced Brain - Extends the existing Brain with quantum processing capabilities
"""
from typing import Dict, List, Any, Optional
import time
from core.brain.brain import Brain
from .quantum.quantum_processor import QuantumProcessorImpl
from .data_models import QuantumThought


class QuantumBrain(Brain):
    """Enhanced Brain with quantum processing capabilities"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quantum_processor = None
        self.quantum_enabled = False
        self._init_quantum_processor()
    
    def _init_quantum_processor(self) -> None:
        """Initialize the quantum processor"""
        try:
            self.quantum_processor = QuantumProcessorImpl(self)
            if self.quantum_processor.activate():
                self.quantum_enabled = True
                print("🔥 Quantum processing capabilities activated!")
            else:
                print("⚠️ Quantum processor failed to activate")
        except Exception as e:
            print(f"❌ Failed to initialize quantum processor: {e}")
            self.quantum_enabled = False
    
    def quantum_think(self, problem: str, max_paths: int = 100, use_quantum: bool = True) -> Dict[str, Any]:
        """
        Quantum-enhanced thinking that processes multiple solution paths in parallel
        
        Args:
            problem: The problem to solve
            max_paths: Maximum number of parallel solution paths to generate
            use_quantum: Whether to use quantum processing (fallback to regular think if False)
        
        Returns:
            Dictionary containing quantum analysis results
        """
        if not use_quantum or not self.quantum_enabled:
            # Fallback to regular thinking
            regular_response = self.think(problem)
            return {
                'problem': problem,
                'solution': regular_response,
                'quantum_enabled': False,
                'processing_time': 0.0,
                'confidence': 0.7,
                'method': 'regular_thinking'
            }
        
        start_time = time.time()
        
        try:
            # Use quantum processor for enhanced thinking
            quantum_result = self.quantum_processor.quantum_think(problem, max_paths)
            processing_time = time.time() - start_time
            
            # Enhance the result with additional metadata
            quantum_result.update({
                'quantum_enabled': True,
                'processing_time': processing_time,
                'method': 'quantum_thinking',
                'quantum_advantage_achieved': quantum_result.get('quantum_advantage', False)
            })
            
            return quantum_result
            
        except Exception as e:
            print(f"Quantum thinking failed: {e}")
            # Fallback to regular thinking
            regular_response = self.think(problem)
            return {
                'problem': problem,
                'solution': regular_response,
                'quantum_enabled': False,
                'processing_time': time.time() - start_time,
                'confidence': 0.7,
                'method': 'fallback_thinking',
                'error': str(e)
            }
    
    def analyze_with_probability(self, problem: str, perspectives: List[str] = None) -> Dict[str, Any]:
        """
        Analyze a problem from multiple perspectives with probability weighting
        
        Args:
            problem: The problem to analyze
            perspectives: List of perspectives to consider (technical, business, ethical, etc.)
        
        Returns:
            Multi-dimensional analysis with probability scores
        """
        if perspectives is None:
            perspectives = ['technical', 'business', 'ethical', 'long_term']
        
        if not self.quantum_enabled:
            # Simple fallback analysis
            analysis = self.think(f"Analyze this problem from {', '.join(perspectives)} perspectives: {problem}")
            return {
                'problem': problem,
                'analysis': analysis,
                'perspectives': perspectives,
                'quantum_enabled': False
            }
        
        # Generate quantum thoughts for each perspective
        perspective_analyses = {}
        all_thoughts = []
        
        for perspective in perspectives:
            perspective_problem = f"Analyze from {perspective} perspective: {problem}"
            thoughts = self.quantum_processor.process_quantum_thoughts(perspective_problem, max_paths=20)
            
            if thoughts:
                best_thought = max(thoughts, key=lambda t: t.probability_score * t.confidence_level)
                perspective_analyses[perspective] = {
                    'analysis': ' '.join(best_thought.solution_path),
                    'confidence': best_thought.confidence_level,
                    'probability': best_thought.probability_score,
                    'risk_factors': best_thought.risk_factors,
                    'success_metrics': best_thought.success_metrics
                }
                all_thoughts.extend(thoughts)
        
        # Synthesize overall solution
        if all_thoughts:
            synthesized = self.quantum_processor.synthesize_solutions(all_thoughts)
            overall_confidence = synthesized.confidence_level
        else:
            overall_confidence = 0.5
        
        return {
            'problem': problem,
            'perspectives': perspective_analyses,
            'overall_confidence': overall_confidence,
            'quantum_enabled': True,
            'total_thoughts_analyzed': len(all_thoughts)
        }
    
    def predict_outcomes(self, scenario: str, variables: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Predict outcomes for a given scenario with confidence intervals
        
        Args:
            scenario: The scenario to analyze
            variables: Variables that might affect the outcome
        
        Returns:
            Prediction results with confidence intervals
        """
        if variables is None:
            variables = {}
        
        if not self.quantum_enabled:
            prediction = self.think(f"Predict outcomes for: {scenario}")
            return {
                'scenario': scenario,
                'prediction': prediction,
                'confidence_interval': (0.3, 0.7),
                'quantum_enabled': False
            }
        
        # Generate multiple outcome scenarios
        outcome_thoughts = self.quantum_processor.process_quantum_thoughts(
            f"Predict possible outcomes for: {scenario} with variables: {variables}",
            max_paths=50
        )
        
        if not outcome_thoughts:
            return {
                'scenario': scenario,
                'prediction': 'Unable to generate predictions',
                'confidence_interval': (0.0, 0.1),
                'quantum_enabled': True,
                'error': 'No quantum thoughts generated'
            }
        
        # Group outcomes by probability ranges
        high_prob_outcomes = [t for t in outcome_thoughts if t.probability_score > 0.7]
        medium_prob_outcomes = [t for t in outcome_thoughts if 0.4 <= t.probability_score <= 0.7]
        low_prob_outcomes = [t for t in outcome_thoughts if t.probability_score < 0.4]
        
        # Calculate weighted predictions
        outcomes = []
        for category, thoughts in [
            ('high_probability', high_prob_outcomes),
            ('medium_probability', medium_prob_outcomes),
            ('low_probability', low_prob_outcomes)
        ]:
            if thoughts:
                avg_confidence = sum(t.confidence_level for t in thoughts) / len(thoughts)
                avg_probability = sum(t.probability_score for t in thoughts) / len(thoughts)
                combined_solution = ' | '.join([' '.join(t.solution_path[:2]) for t in thoughts[:3]])
                
                outcomes.append({
                    'category': category,
                    'prediction': combined_solution,
                    'probability': avg_probability,
                    'confidence': avg_confidence,
                    'count': len(thoughts)
                })
        
        # Overall confidence interval
        all_probs = [t.probability_score for t in outcome_thoughts]
        min_prob = min(all_probs) if all_probs else 0.0
        max_prob = max(all_probs) if all_probs else 1.0
        
        return {
            'scenario': scenario,
            'variables': variables,
            'outcomes': outcomes,
            'confidence_interval': (min_prob, max_prob),
            'quantum_enabled': True,
            'total_scenarios_analyzed': len(outcome_thoughts)
        }
    
    def get_quantum_status(self) -> Dict[str, Any]:
        """Get the status of quantum processing capabilities"""
        if not self.quantum_enabled or not self.quantum_processor:
            return {
                'quantum_enabled': False,
                'status': 'disabled',
                'reason': 'Quantum processor not available'
            }
        
        return {
            'quantum_enabled': True,
            'status': 'active',
            'processor_status': self.quantum_processor.get_status(),
            'performance_metrics': self.quantum_processor.performance_metrics
        }
    
    def enable_quantum_mode(self) -> bool:
        """Enable quantum processing mode"""
        if not self.quantum_processor:
            self._init_quantum_processor()
        
        if self.quantum_processor and not self.quantum_enabled:
            self.quantum_enabled = self.quantum_processor.activate()
        
        return self.quantum_enabled
    
    def disable_quantum_mode(self) -> None:
        """Disable quantum processing mode"""
        self.quantum_enabled = False
        if self.quantum_processor:
            self.quantum_processor.deactivate()
    
    def shutdown(self) -> None:
        """Shutdown quantum capabilities"""
        if self.quantum_processor:
            self.quantum_processor.shutdown()
        self.quantum_enabled = False