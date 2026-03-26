"""
Test package for models.
"""

from .test_user import TestUserModel, TestUserEdgeCases
from .test_agent import TestAgentModel, TestAgentStatusTransitions, TestAgentCronManagement, TestAgentEdgeCases
from .test_session import TestSessionModel, TestSessionStatistics, TestSessionEdgeCases, TestSessionEdgeCases2
from .test_task import TestTaskModel, TestTaskStatusTransitions, TestTaskAssignments, TestTaskGitHubIntegration, TestTaskEdgeCases
from .test_activity_event import TestActivityEventModel, TestActivityEventEdgeCases, TestActivityEventTypeValues, TestActivityEventUpdate
from .test_approval import TestApprovalModel, TestApprovalWorkflow, TestApprovalTypes, TestApprovalEdgeCases
from .test_memory_entry import TestMemoryEntryModel, TestMemoryEntryWorkflow, TestMemoryEntryTypes, TestMemoryEntryEdgeCases
from .test_metric import TestMetricModel, TestMetricScenarios, TestMetricEdgeCases
from .test_repository import TestRepositoryModel, TestRepositoryStatus, TestRepositoryEdgeCases
from .test_cron_execution import TestCronExecutionModel, TestCronExecutionScenarios, TestCronExecutionEdgeCases
from .test_sdd_artifact import TestSddArtifactModel, TestSddArtifactWorkflow, TestSddArtifactTypes, TestSddArtifactEdgeCases

__all__ = [
    # User
    "TestUserModel",
    "TestUserEdgeCases",
    # Agent
    "TestAgentModel",
    "TestAgentStatusTransitions",
    "TestAgentCronManagement",
    "TestAgentEdgeCases",
    # Session
    "TestSessionModel",
    "TestSessionStatistics",
    "TestSessionEdgeCases",
    "TestSessionEdgeCases2",
    # Task
    "TestTaskModel",
    "TestTaskStatusTransitions",
    "TestTaskAssignments",
    "TestTaskGitHubIntegration",
    "TestTaskEdgeCases",
    # Activity Event
    "TestActivityEventModel",
    "TestActivityEventEdgeCases",
    "TestActivityEventTypeValues",
    "TestActivityEventUpdate",
    # Approval
    "TestApprovalModel",
    "TestApprovalWorkflow",
    "TestApprovalTypes",
    "TestApprovalEdgeCases",
    # Memory Entry
    "TestMemoryEntryModel",
    "TestMemoryEntryWorkflow",
    "TestMemoryEntryTypes",
    "TestMemoryEntryEdgeCases",
    # Metric
    "TestMetricModel",
    "TestMetricScenarios",
    "TestMetricEdgeCases",
    # Repository
    "TestRepositoryModel",
    "TestRepositoryStatus",
    "TestRepositoryEdgeCases",
    # Cron Execution
    "TestCronExecutionModel",
    "TestCronExecutionScenarios",
    "TestCronExecutionEdgeCases",
    # SDD Artifact
    "TestSddArtifactModel",
    "TestSddArtifactWorkflow",
    "TestSddArtifactTypes",
    "TestSddArtifactEdgeCases",
]
