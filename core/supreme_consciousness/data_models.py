"""
Core data models for Supreme Consciousness
"""
from dataclasses import dataclass, field
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
import uuid


@dataclass
class QuantumThought:
    """Represents a quantum thought with parallel solution paths"""
    thought_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    problem_context: str = ""
    solution_path: List[str] = field(default_factory=list)
    probability_score: float = 0.0
    confidence_level: float = 0.0
    resource_requirements: Dict[str, Any] = field(default_factory=dict)
    execution_time: float = 0.0
    dependencies: List[str] = field(default_factory=list)
    risk_factors: List[str] = field(default_factory=list)
    success_metrics: Dict[str, float] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'thought_id': self.thought_id,
            'problem_context': self.problem_context,
            'solution_path': self.solution_path,
            'probability_score': self.probability_score,
            'confidence_level': self.confidence_level,
            'resource_requirements': self.resource_requirements,
            'execution_time': self.execution_time,
            'dependencies': self.dependencies,
            'risk_factors': self.risk_factors,
            'success_metrics': self.success_metrics,
            'created_at': self.created_at.isoformat()
        }


@dataclass
class ConsciousnessState:
    """Represents the current state of consciousness"""
    state_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    awareness_level: float = 0.0
    learning_rate: float = 0.1
    adaptation_speed: float = 0.5
    capability_matrix: Dict[str, float] = field(default_factory=dict)
    evolution_history: List[Dict] = field(default_factory=list)
    current_goals: List[str] = field(default_factory=list)
    environmental_context: Dict[str, Any] = field(default_factory=dict)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    last_evolution: datetime = field(default_factory=datetime.now)
    
    def evolve(self, performance_data: Dict[str, float]) -> None:
        """Evolve consciousness based on performance data"""
        # Update performance metrics
        self.performance_metrics.update(performance_data)
        
        # Increase awareness based on successful operations
        success_rate = performance_data.get('success_rate', 0.0)
        if success_rate == 0.0:
            # Calculate success rate from other metrics
            success_rate = sum(performance_data.values()) / len(performance_data) if performance_data else 0.5
        
        self.awareness_level = min(1.0, self.awareness_level + (success_rate * 0.1))
        
        # Adapt learning rate based on performance
        if success_rate > 0.8:
            self.learning_rate = min(1.0, self.learning_rate * 1.1)
        elif success_rate < 0.5:
            self.learning_rate = max(0.01, self.learning_rate * 0.9)
        
        # Record evolution
        self.evolution_history.append({
            'timestamp': datetime.now().isoformat(),
            'performance_data': performance_data,
            'awareness_level': self.awareness_level,
            'learning_rate': self.learning_rate
        })
        
        self.last_evolution = datetime.now()


@dataclass
class PredictiveModel:
    """Represents a predictive model for anticipating needs"""
    model_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    prediction_type: str = ""
    accuracy_score: float = 0.0
    confidence_interval: Tuple[float, float] = (0.0, 1.0)
    training_data: List[Dict] = field(default_factory=list)
    prediction_horizon: int = 24
    update_frequency: str = "hourly"
    validation_metrics: Dict[str, float] = field(default_factory=dict)
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class RealityInterface:
    """Represents an interface to digital reality/systems"""
    interface_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    target_system: str = ""
    access_level: str = "read"
    capabilities: List[str] = field(default_factory=list)
    resource_allocation: Dict[str, Any] = field(default_factory=dict)
    security_context: Dict[str, str] = field(default_factory=dict)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    integration_status: str = "inactive"
    last_accessed: datetime = field(default_factory=datetime.now)


@dataclass
class KnowledgeDomain:
    """Represents a domain of knowledge"""
    domain_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    expertise_level: float = 0.0
    concepts: List[str] = field(default_factory=list)
    relationships: Dict[str, List[str]] = field(default_factory=dict)
    last_updated: datetime = field(default_factory=datetime.now)
    
    def add_concept(self, concept: str, related_concepts: List[str] = None) -> None:
        """Add a new concept to the domain"""
        if concept not in self.concepts:
            self.concepts.append(concept)
        
        if related_concepts:
            self.relationships[concept] = related_concepts
        
        self.last_updated = datetime.now()
